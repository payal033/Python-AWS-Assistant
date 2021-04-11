import pyttsx3
import speech_recognition as sr
import os
import datetime
import sys

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices') 
engine.setProperty('voice',voices[1].id) # voices[1] denotes female voice

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def aboutMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning")
    elif hour >=12 and hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    
    speak("I am your Assistant Joana. I can help you with AWS management console and can help you to create instances, launch and describe them very easily")
    print('''
----------------------------------------------------------------------------------------------------------------------------------------------
1. Launch Instance
2. Create Key Pair
3. Create Securtiy Group
4. Create Volume
5. Attach Volume
6. Show Status of Instance
7. Start Instances
8. Stop Instances
9. Terminate Instance
10. Describe instance Details
------------------------------------------------------------------------------------------------------------------------------------------------
''')

    speak('These are list of tasks which I can perform')


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 200
        r.adjust_for_ambient_noise(source,duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("You said: " + query)
    except Exception as e:
        print("Can you repeat that again please..!")
        return "None"
    return query


def showSecurityGroups():
	os.system('aws ec2 describe-security-groups  --query "SecurityGroups[*].{Name:GroupName}" --output text')


def showKeyPairs():
	os.system('aws ec2 describe-key-pairs --query "KeyPairs[*].{Name:KeyName}" --output text')

def showVolumes():
	os.system('aws ec2 describe-volumes --query "Volumes[*].{ID:VolumeId,Tag:Tags}"')

def showInstances():
	os.system("aws ec2 describe-instances --filters Name=instance-type,Values=t2.micro --query \"Reservations[*].Instances[*].{Instance:InstanceId,AZ:Placement.AvailabilityZone,Name:Tags[?Key=='Name']|[0].Value}\"")

def executeTask(query):

	if 'key' in query or 'pair' in query or 'key pair' in query:

		print("Creating AWS Key Pair")
		speak("Creating AWS Key Pair")

		print("What name would you like to give?Enter name")
		speak("What name you would like to give")

		keyname = input()

		print("Creating key pair")
		os.system('aws ec2 create-key-pair --key-name {}'.format(keyname))

		print('Your key {} created successfully'.format(keyname))
		speak('Your key {} created successfully'.format(keyname))

	elif 'security' in query or 'group' in query or 'security group' in query:

		print("Creating AWS Security Group")
		speak("Creating AWS Security group")

		print("What name would you like to give?Enter name")
		speak("What name you would like to give? Enter name")

		sgname = input()

		print("Provide some description for your security group..Speak")
		speak("Provide some description for your security group..Speak")

		sgdesc = takeCommand()

		print("Creating Security Group")
		os.system('aws ec2 create-security-group --group-name {} --description "{}"'.format(sgname,sgdesc))

		print('Your Security Group {} created successfully'.format(sgname))
		speak('Your Security Group {} created successfully'.format(sgname))

	elif 'volume' in query and 'create' in query:

		print('Creating Volume')
		speak('Creating Volume')

		print('What name you would like to give?Enter name')
		speak('What name you would like to give?Enter name')

		vname = input()

		print('Okay! Please enter size of your volume in GB')
		speak('Okay! Please enter size of your volume in GB')

		vsize = input()

		os.system("aws ec2 create-volume --availability-zone us-east-1a --size "+vsize+" --tag-specifications ResourceType=volume,Tags=[{Key=Name,Value="+vname+"}]")

		print('You volume of size {}GB has been created successfully'.format(vsize))
		speak('You volume of size {}GB has been created successfully'.format(vsize))

	elif 'attach' in query and 'volume' in query:

		print('Lets attach volume to instance')
		speak('Lets attach volume to instance')

		print('Which volume you would like to attach?These are some of the volumes available')
		speak('Which volume you would like to attach?These are some of the volumes available')

		showVolumes()

		print('Enter volume Id')
		speak('Enter volume Id')

		vid = input()

		print('Please specify instance to which you would like to attach volume? These are some of instances available')
		speak('Please specify instance to which you would like to attach volume? These are some of instances available')

		showInstances()

		print('Enter Instance Id')
		speak('Enter Instance Id')

		instId = input()

		print('Attaching volume..')
		speak('Attaching volume')

		os.system('aws ec2 attach-volume --volume-id {} --instance-id {} --device /dev/sdf'.format(vid,instId))

		print('Volume attached successfully')
		speak('Volume attached successfully')

	elif 'start instance' in query or 'start' in query:

		print('These are list of instances  which are stopped')
		speak('These are list of instances  which are stopped')

		os.system("aws ec2 describe-instances --query \"Reservations[*].Instances[*].{Instance:InstanceId,Name:Tags[?Key=='Name']|[0].Value,Status:State.Name}\" --filters Name=instance-state-name,Values=stopped")

		print('Enter instance Id to start your instance..')
		speak('Enter instance Id to start your instance..')

		intid = input()

		print('Starting instance')
		speak('Starting Instance')

		os.system('aws ec2 start-instances --instance-ids {}'.format(intid))

		print('Instance id {} started successfully'.format(intid))
		speak('Instance id {} started successfully'.format(intid))

	elif 'stop instance' in query or 'stop' in query:

		print('These are list of instances which are running')
		speak('These are list of instances which are running')

		os.system("aws ec2 describe-instances --query \"Reservations[*].Instances[*].{Instance:InstanceId,Name:Tags[?Key=='Name']|[0].Value,Status:State.Name}\" --filters Name=instance-state-name,Values=running")

		print('Enter instance Id to stop your instance..')
		speak('Enter instance Id to stop your instance..')

		intid = input()

		print('Stopping instance')
		speak('Stopping Instance')

		os.system('aws ec2 stop-instances --instance-ids {}'.format(intid))

		print('Instance id {} stopped successfully'.format(intid))
		speak('Instance id {} stopped successfully'.format(intid))

	elif 'status' in query or 'state' in query:

		print('Instances in Running state are as follows')
		speak('Instances in Running state are as follows')

		os.system("aws ec2 describe-instances --query \"Reservations[*].Instances[*].{Instance:InstanceId,Name:Tags[?Key=='Name']|[0].Value,Status:State.Name}\" --filters Name=instance-state-name,Values=running")

		print('Instances in Stopped state are as follows')
		speak('Instances in Stopped state are as follows')

		os.system("aws ec2 describe-instances --query \"Reservations[*].Instances[*].{Instance:InstanceId,Name:Tags[?Key=='Name']|[0].Value,Status:State.Name}\" --filters Name=instance-state-name,Values=stopped")

	elif "list" in query or "detail" in query or "details" in query:

		print("Detail about all the instances:")
		speak("Detail about all the instances:")

		os.system("aws ec2 describe-instances --instance-ids --query \"Reservations[*].Instances[*].{LaunchTime:LaunchTime,Instance:InstanceId,ImageId:ImageId,VolumeInfo:BlockDeviceMappings,SubnetId:SubnetId,AvailabilityZone:Placement.AvailabilityZone,PublicIP:PublicIpAddress Name:Tags[?Key=='Name']|[0].Value,Status:State.Name}\" --filters Name=instance-state-name,Values=stopped,running")

		print('These are details of all instances')
		speak('These are details of all instances')

	elif "terminate" in query:

		print("Instance Details")
		speak('These are instance details')

		showInstances()
		
		print("Enter Instance Id of Instance you wish to terminate")
		speak("Enter Instance Id of Instance you wish to terminate")

		i=input()
		os.system("aws ec2 terminate-instances --instance-ids "+i)

		speak("Your Instance has terminated.")
		speak("You can check your AWS Console")

	elif 'launch instance' in query or 'create instance' in query or 'launch' in query:
		print('Okay! Lets launch AWS EC2 instance')
		speak('Okay! Lets launch AWS EC2 instance')

		speak('Which AMI would you like to use?')
		amis = ['Amazon Linux 2 AMI (HVM), SSD Volume Type','Red Hat Enterprise Linux 8 (HVM), SSD Volume Type',
		'Ubuntu Server 20.04 LTS (HVM), SSD Volume Type','Microsoft Windows Server 2019 Base','Debian 10 (HVM), SSD Volume Type']
		print('''
1. Amazon Linux 2 AMI (HVM), SSD Volume Type - ami-0742b4e673072066f (64-bit x86)
2. Red Hat Enterprise Linux 8 (HVM), SSD Volume Type - ami-096fda3c22c1c990a (64-bit x86)
3. Ubuntu Server 20.04 LTS (HVM), SSD Volume Type - ami-042e8287309f5df03 (64-bit x86) 
4. Microsoft Windows Server 2019 Base - ami-07817f5d0e3866d32
5. Debian 10 (HVM), SSD Volume Type - ami-07d02ee1eeb0c996c (64-bit x86)
		''')
		print('Enter your choice')
		choice = int(input())

		if choice == 1:
			amiId = 'ami-0742b4e673072066f'
		elif choice == 2:
			amiId = 'ami-096fda3c22c1c990a'
		elif choice == 3:
			amiId = 'ami-042e8287309f5df03'
		elif choice == 4:
			amiId = 'ami-07817f5d0e3866d32'
		elif choice == 5:
			amiId = 'ami-07d02ee1eeb0c996c'

		print('You selected {} as your AMI'.format(amis[choice-1]))
		speak('You selected {} as your AMI'.format(amis[choice-1]))
		
		print('Your default Instance Type is t2.micro')
		speak('Your default Instance Type is t2.micro')

		speak('How many instances you would like to launch? Enter number')
		print('How many instances you would like to launch? Enter number')

		instanceCount = input()

		print('Default subnet in any availability zone is selected')
		speak('Default subnet in any availability zone is selected')

		print('Creating volume of size 8GB')
		speak('Creating volume of size 8GB')

		print('What name would you like to give to your instance?Enter name')
		speak('What name would you like to give to your instance?Enter name')

		instanceName = input()

		print('Your instance name is',instanceName)
		speak('Your instance name is {}'.format(instanceName))

		print('Which security group you would like to attach? These are some of the Security Groups available')
		speak('Which security group you would like to attach? These are some of the Security Groups available')
		showSecurityGroups()
		print('Enter name')
		speak('Enter name')

		sg = input()

		print('Your Security Group name',sg,"is attached")
		speak('Your Security Group name {} is attached'.format(sg))

		print('Which key pair would you like to attach?These are some of the available Key pairs')
		speak('Which key pair would you like to attach?These are some of the available Key pairs')
		showKeyPairs()
		print('Enter name')
		speak('Enter name')

		keyPairName = input()

		print('Your Key pair name',keyPairName,'is connected')
		speak('Your Key pair name {} is connected'.format(keyPairName))

		print('Launching Instance')
		speak('Launching Instance')

		runquery = "aws ec2 run-instances --image-id " +amiId+ " --key-name " +keyPairName+" --tag-specifications ResourceType=instance,Tags=[{Key=Name,Value="+instanceName+"}] --security-groups "+sg+" --instance-type t2.micro --placement AvailabilityZone=us-east-1a --count "+instanceCount
		os.system(runquery)

		print('Your instance has been launched successfully')
		speak('Your instance has been launched successfully')


	elif 'bye' in query or 'exit' in query:
		speak("Bye Have a great Day!!")
		os.system('cls')
		sys.exit()


if __name__ == "__main__":
	aboutMe()
	speak('Tell me what can I do for you?')
	while True:
		query = takeCommand().lower()
		executeTask(query)



