1 put cloudwatchagent-windows-config.json in s3 bucket get bucket public
2 change path to s3 bucket in install-cloudwatchagent-windows.ps1
3 connect to rdp session in windows EC2 instance run script 
  Cloud watch agent installed and configured 
4 login to aws console and create sns topic or copy arn exist arn 
5 move to cloudformation and create new stack upload numerix-windows-cloudwatch-alarms.yaml
  chose instance . put frendly name instance. arn sns topic and create
6 repeat step for alarm Disk space 
  it's short instruction for creade monitiring and alarm for windows instance 