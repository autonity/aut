import os
import subprocess
import time

def main():
    # Set the environment variable
    os.environ['KEYFILEPWD'] = 'yourpassword'

    # Replace YOUR_ADDRESS with the actual address
    to_address = 'YOUR_ADDRESS'

    while True:
        # Create the transaction command
        make_cmd = ['aut', 'tx', 'make', '--to', to_address, '--value', '1']
        sign_cmd = ['aut', 'tx', 'sign', '-']
        send_cmd = ['aut', 'tx', 'send', '-']

        
        make_process = subprocess.Popen(make_cmd, stdout=subprocess.PIPE)
        sign_process = subprocess.Popen(sign_cmd, stdin=make_process.stdout, stdout=subprocess.PIPE)
        make_process.stdout.close()  
        send_process = subprocess.Popen(send_cmd, stdin=sign_process.stdout)
        sign_process.stdout.close()  

        
        send_process.communicate()

        # Wait for 1.7 seconds before the next iteration
        time.sleep(1.7)

if __name__ == '__main__':
    main()
