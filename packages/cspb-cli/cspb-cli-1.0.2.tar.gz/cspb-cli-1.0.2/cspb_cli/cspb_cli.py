# Copyright 2021 Gerard L. Muir 
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
from queue import PriorityQueue
from termios import TIOCPKT_DOSTOP
from cmd2 import Cmd
from cspb.CSPB import CSPB
import os
import smbus
import time
import math
import getopt
import sys
 
class pb_cli(Cmd):
    """ 
    This class provides a command line interface to communicate to the Cluster System Power Board (CSPB).
    
    Attributes
    ----------
    
    Methods
    -------
    
    
    Author: Gerard L. Muir
    """
    
    prompt = 'cspb_cntl-> '
    intro = "\n Welcome to the Cluster System Power Board command line tool! Type ? for available commands. \n"
    completekey = 'tab'
    power_board = None
    valid_slot_numbers = [1,2,3,4]


    def do_exit(self, inp):
        print("Bye")
        return True
    
    def help_exit(self):
        print('')
        print('Exit the application.')

    def emptyline(self): 
        pass # Override Cmd class emptyline method to disable repeating last command automatically.
 
    def do_connect(self, inp):
        # Connects to  the specified i2c buss address.
        user_input = inp.split(' ')
        bus_number = int(user_input[0])
        i2c_address = int(user_input[1])

        try:
            self.power_board = CSPB(bus_number, i2c_address)
        except (PermissionError, FileNotFoundError):
            print('Connection Error, check addresses.')

    def help_connect(self):
        print('')
        print('Opens a communicatin link to the device at the secified i2c address.')
        print('')
        print('Usage: connect device_i2c_buss_number device_i2c_address')
        print('')
        print('Example: connect 1 15')
        print('')
        print('Note: Use the "scan" command for list of i2c devices.')


    def do_power(self, inp):
        # Powers on or off the specified power slot.
        if self.power_board is None:
            print('No active connection.')
        else:
            valid_power_states = ['on', 'off']
            args = inp.split()
            power_state = args[0]
            if power_state in valid_power_states: 
                slot_numbers = args[1].split(',')
                if len(slot_numbers) > 0:
                    for slot_number in slot_numbers:
                        if int(slot_number) in self.valid_slot_numbers:
                            current_power_state = self.power_board.read_register(self.power_board.PWR_STTS_RGSTR_ADDR)
                            if power_state == 'on':
                                new_power_state = current_power_state | (1 << (int(slot_number) -1))
                            elif power_state == 'off':
                                new_power_state = current_power_state & (~(1 << (int(slot_number)-1)))
                            self.power_board.set_power(new_power_state)
                        else:
                            print('Slot number ', slot_number, 'is invalid.')
            else:
                self.help_power()

 
    def help_power(self):
        print('')
        print('Turn power ON or OFF for the specified power slot.')
        print('WARRNING - This command does not signal shutdown.')
        print('')
        print('Usage: power power_state slot_number')
        print('    power_state: on | off')
        print('    slot_number: comma seperated list of slot numbers from 1 through 4')
        print('')
        print('Example: Apply power to slot two.')
        print('power on 2' )
        print('')
        print('Example: Apply power to slot three and four.')
        print('power on 3,4' )
        print('')
        print('Example: Remove power from slot two.')
        print('power off 2' )
        print('')

    def do_signal_shutdown(self, inp):
        # Signal shutdown only to the SBC. Does not remove power to the slot.
        if self.power_board is None:
            print('No active connection.')
        else:
            slot_numbers = inp.split(',')
            if len(slot_numbers) > 0:
                for slot_number in slot_numbers:
                    if int(slot_number) in self.valid_slot_numbers:
                        slot_value =  self.get_slot_byte_value(slot_number)
                        self.power_board.signal_shutdown(slot_value)
                    else:
                        print('Slot number ', slot_number, 'is invalid.')
            else:
                self.help_signal_shutdown()

    def help_signal_shutdown(self):
        print('')
        print("Sends the shutdown signal only to the specified power slot.")
        print('')
        print('Usage: signal_shutdown slot_number')
        print('    slot_number: comma seperated list of slot numbers from 1 through 4')
        print('')
        print('Example: Apply shutdown signal to slot two.')
        print('signal_shutdown 2' )
        print('')
        print('Example: Apply shutdown signal to slot three and four.')
        print('signal_shutdown on 3,4' )
        print('')

    def do_shutdown(self, inp):
        # Executes a proper shutdown and power removal to the specified slot.
        if self.power_board is None:
            print('No active connection.')
        else:
            slot_numbers = inp.split(',')
            if len(slot_numbers) > 0:
                for slot_number in slot_numbers:
                    if int(slot_number) in self.valid_slot_numbers:
                        shutdown_timeout = self.power_board.read_register(self.power_board.SHTDWN_TIME_OUT_RGSTR_ADDR) # already in seconds.
                        power_down_hold_delay = (self.power_board.read_register(self.power_board.PWR_DWN_SGNL_DRTN_RGSTR_ADDR)*20)/1000 # convert from miliseconds to seconds.
                        max_trys = math.ceil(shutdown_timeout + power_down_hold_delay +1)
                        slot_value =  self.get_slot_byte_value(slot_number)
                        self.power_board.shutdown(slot_value)
                        for attempt in range(max_trys): # Wait for the CSPB to process the shutdown command
                            print(".",  sep=' ', end='', flush=True)
                            time.sleep(1)
                            try:
                                is_shutting_down = self.power_board.read_register(self.power_board.IN_SHUTDOWN_RGSTR_ADDR) # actually any read command will do.
                                if (is_shutting_down == 0):
                                    break # exit monitor loop if shutdown complere.
                            except IOError:
                               pass # still waiting for shutdown process to finish.
                        print(" ")
                    else:
                        print('Slot number ', slot_number, 'is invalid.')
            else:
                self.help_shutdown()

    def help_shutdown(self):
        print('')
        print("Signals shutdown to the SBC in the specified slot and then removes power to that slot." )
        print('')
        print('Usage: shutdown slot_number')
        print('    slot_number: comma seperated list of slot numbers from 1 through 4')
        print('')
        print('Example: Shutdown slot two.')
        print('shutdown 2' )
        print('')
        print('Example: Shutdown slot three and four.')
        print('shutdown on 3,4' )
        print('')

    def do_read_reg(self, inp):
        # Reads and prints the specified power board register. 
        if self.power_board is None:
            print('No active connection.')
        else:
            register_address = int(inp)
            self.power_board.set_register_number(register_address)
            register_value = self.power_board.read_register(register_address)
            print(register_value)

    def help_read_reg(self):
        print('')
        print("Reads the current value of the specified register." )
        print('')
        print('Usage: read_reg register_number')
        print('    register_number: 0 through 128')
        print('')
        print('Example: Read the value of register 0')
        print('read_reg 0' )
        print('')
        print('Note: See the product user manual for details on register usage.')
        print('')


    def do_write_reg(self, inp):
        # Writes the provided value to the specified register. 
        if self.power_board is None:
            print('No active connection.')
        else:
            args = inp.split()
            if len(args) == 2:
                register_address = args[0]
                value = args[1]
                self.power_board.write_register(int(register_address), int(value))
            else:
                self.help_write_reg()

    def help_write_reg(self):
        print('')
        print("Writes the supplied value to the specified register." )
        print('')
        print('Usage: write_reg register_number value')
        print('    register_number: 0 through 128')
        print('    value: 0-255')
        print('')
        print('Example: Write the value 3 to register 0')
        print('write_reg 0 3' )
        print('')
        print('Note: See the product user manual for details on register usage.')
        print('')

    def do_dump_registers(self, inp):
        # Prints out the value of all power board registers.
        if self.power_board is None:
            print('No active connection.')
        else:
            for register in range(0, 129):
                try:
                    self.power_board.set_register_number(register)
                    time.sleep(.1)
                    register_value = self.power_board.read_register(register)
                    print(f'Register: ' , register , 'Value: ' , register_value)
                    time.sleep(.05)
                except OSError:
                    print('Read error on register: ', register)
                    
                
    def help_dump_registers(self):
        print('')
        print("Prints the value of all CSPB registers." )
        print('')
        print('Usage: dump_registers')
        print('')

    def do_scan(self, inp):
        # Scans the i2c bus for i2c nodes and prints available nodes.
        self.get_available_i2c_bus_numbers()
    
    def help_scan(self):
        print('')
        print("Prints a list of available i2c busses and i2c devices on the bus." )
        print('')
        print('Usage: scan')
        print('')

    def default(self, inp):
        print("Error: {}".format(inp) + " not recognized")

    # do_EOF = do_exit
    # help_EOF = help_exit

    def get_available_i2c_bus_numbers(self):
        # Prints a list available i2c busses on system.
        for i2c_num in range (0, 10):
            file_path = "/dev/i2c-"
            file_path  += str(i2c_num)
            if os.path.exists(file_path):
                print("Bus number: " + str(i2c_num) )
                try:
                    bus = smbus.SMBus(i2c_num)
                    for addr in range (8, 178):
                        try:
                            bus.write_quick(addr)
                            print("Device address: " + str(addr) + " ")
                        except IOError:
                            pass
                except:
                    pass
        return 
 
    def get_slot_byte_value(self, slot_number):
    # Convert the slot number to a byte position.
    # Example: slot 2 returns 0010
    #          slot 3 returns 0100
        return 1 << (int(slot_number) -1)

if __name__ == '__main__':
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"v")
    except getopt.GetoptError:
        print('cspb_cli.py -v')
        sys.exit(2)                
    
    pb_cli().cmdloop()
    
