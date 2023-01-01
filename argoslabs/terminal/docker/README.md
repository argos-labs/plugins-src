# Docker Remote Service

***This plugin try to connect remote host and run docker or docker-compose service.***

> This function is one of Plugins Operation.You can find the movie in [ARGOS RPA+ video tutorial](https://www.argos-labs.com/video-tutorial/).

## Name of the plugin
Item | Value
---|:---:
Icon | ![Icon](icon.png) 
Display Name | **Docker Remote Service**

## Name of the author (Contact info of the author)

Jerry Chae
* [email](mailto:mcchae@argos-labs.com)
* [github](https://github.com/Jerry-Chae)

## Notification

### Dependent modules
Module | Source Page | License | Version (If specified otherwise using recent version will be used)
---|---|---|---
[paramiko](https://pypi.org/project/paramiko/) | [paramiko/paramiko](https://github.com/paramiko/paramiko) | [LGPL v2.1](https://github.com/paramiko/paramiko/blob/main/LICENSE) | 2.10.4
[paramiko-expect](https://pypi.org/project/paramiko-expect/) | [fgimian/paramiko-expect](https://github.com/fgimian/paramiko-expect) | [MIT](https://github.com/fgimian/paramiko-expect/blob/master/LICENSE) | 0.3.2
[cryptography](https://pypi.org/project/cryptography/) | [pyca/cryptography](https://github.com/pyca/cryptography/) | [Both Apache BSD License](https://github.com/pyca/cryptography/blob/main/LICENSE) | 37.0.0


## Warning 
No potential damage to customer files and data (overwrite risk)

## Helpful links to 3rd party contents
None

## Version Control 
* [4.410.2130](setup.yaml)
* Release Date: `Apr 10, 2022`

## Input (Required)
Display Name | Input Method | Default Value | Description
---|---|---|---
Operation | One of next operations 'Docker Info', 'Docker Command', 'Start Docker Compose', 'Stop Docker Compose', 'State of Docker Compose' | | You can run the docker related operation
SSH Host | | | Host or IP address to connect by SSH
SSH User | | | User for SSH

> * If message to translate is too big then use `Text file`

## Input (Optional)

Display Name | Show Default | Input Method | Default Value | Description
---|---|---|---|---
Command | True | | | When select 'Docker Command' Operation this command is used. (Note: the first docker command is given by system. so if your command is 'docker info' then just enter 'info')
Compose YAML | True | | | When you select one of 'Start Docker Compose', 'Stop Docker Compose', 'State of Docker Compose' operations this docker-compose yaml file must given
Parameters | True | multiple input possible | | When above `Compose YAML` is given the parameter place holder can be `{{key}}`. In this case this parameter expressed by `key::=value` and then replaced with the `value`
Port | False | Integer | 22 | SSH connection port
Password | False | password | | Password for the ssh connection. One of this `pasword` or next `SSH Keyfile` must given
SSH Keyfile | False | | | Private Key file for the ssh connection. One of above `pasword` or this `SSH Keyfile` must given
Prompt RegExp | False | | `{username}@.*\$ ` | This prompt is the shell prompt when you connect the server by ssh
Connect Timeout | False | integer | 10 | Connection timeout for ssh
Prompt Expect timeout | False | integer | 600 | For every execution of command it needed to wait and this duration timeout

> * If Show Default is True then this item is showed at the Properties otherwise hided at Advanced group

## Return Value

This return value may be different by the Operations:

* `Docker Info` : returns the `docker info` with JSON format
> Next is example output for above `Docker Info` operation:
> {"ID":"X6DP:CXSG:U7JA:BWHW:JSEH:YOHR:X3K4:UIEK:35BL:6K6M:ORTK:R3LX","Containers":3,"ContainersRunning":3,"ContainersPaused":0,"ContainersStopped":0,"Images":11,"Driver":"overlay2","DriverStatus":[["Backing Filesystem","extfs"],["Supports d_type","true"],["Native Overlay Diff","true"],["userxattr","false"]],"Plugins":{"Volume":["local"],"Network":["bridge","host","ipvlan","macvlan","null","overlay"],"Authorization":null,"Log":["awslogs","fluentd","gcplogs","gelf","journald","json-file","local","logentries","splunk","syslog"]},"MemoryLimit":true,"SwapLimit":true,"KernelMemory":true,"KernelMemoryTCP":true,"CpuCfsPeriod":true,"CpuCfsQuota":true,"CPUShares":true,"CPUSet":true,"PidsLimit":true,"IPv4Forwarding":true,"BridgeNfIptables":true,"BridgeNfIp6tables":true,"Debug":false,"NFd":52,"OomKillDisable":true,"NGoroutines":61,"SystemTime":"2022-05-16T02:40:03.342566422Z","LoggingDriver":"json-file","CgroupDriver":"cgroupfs","CgroupVersion":"1","NEventsListener":1,"KernelVersion":"5.10.78-4.ph4-esx","OperatingSystem":"VMware Photon OS/Linux","OSVersion":"4.0","OSType":"linux","Architecture":"x86_64","IndexServerAddress":"https://index.docker.io/v1/","RegistryConfig":{"AllowNondistributableArtifactsCIDRs":[],"AllowNondistributableArtifactsHostnames":[],"InsecureRegistryCIDRs":["127.0.0.0/8"],"IndexConfigs":{"docker.io":{"Name":"docker.io","Mirrors":[],"Secure":true,"Official":true}},"Mirrors":[]},"NCPU":2,"MemTotal":2090532864,"GenericResources":null,"DockerRootDir":"/var/lib/docker","HttpProxy":"","HttpsProxy":"","NoProxy":"","Name":"hvrouter","Labels":[],"ExperimentalBuild":false,"ServerVersion":"20.10.11","Runtimes":{"io.containerd.runc.v2":{"path":"runc"},"io.containerd.runtime.v1.linux":{"path":"runc"},"runc":{"path":"runc"}},"DefaultRuntime":"runc","Swarm":{"NodeID":"","NodeAddr":"","LocalNodeState":"inactive","ControlAvailable":false,"Error":"","RemoteManagers":null},"LiveRestoreEnabled":false,"Isolation":"","InitBinary":"docker-init","ContainerdCommit":{"ID":"05f951a3781f4f2c1911b05e61c160e9c30eaa8e","Expected":"05f951a3781f4f2c1911b05e61c160e9c30eaa8e"},"RuncCommit":{"ID":"14faf1c20948688a48edb9b41367ab07ac11ca91","Expected":"14faf1c20948688a48edb9b41367ab07ac11ca91"},"InitCommit":{"ID":"de40ad0","Expected":"de40ad0"},"SecurityOptions":["name=apparmor","name=seccomp,profile=default"],"ProductLicense":"Community Engine","Warnings":null,"ClientInfo":{"Debug":false,"Context":"default","Plugins":[],"Warnings":null}}

* `Docker Command` : returns the docker command output
> Next is the output for the command ***"run --rm hello-world"***
```
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

* `Start Docker Compose` : returns the output of `docker-compose up -d`

```
reating network "guacamole_default" with the default driver
Creating guacdb ... done
Creating guacd  ... done
Creating guacamole ... done
```

* `Stop Docker Compose` : returns the output of `docker-compose down`

```
Stopping guacamole ... done
Stopping guacdb    ... done
Stopping guacd     ... done
Removing guacamole ... done
Removing guacdb    ... done
Removing guacd     ... done
Removing network guacamole_default
```

* `State Docker Compose` : returns the output of `docker-compose ps`

```
  Name                 Command                  State                         Ports                   
------------------------------------------------------------------------------------------------------
guacamole   /opt/guacamole/bin/start.sh      Up             0.0.0.0:18080->8080/tcp,:::18080->8080/tcp
guacd       /bin/sh -c /usr/local/guac ...   Up (healthy)   4822/tcp                                  
guacdb      docker-entrypoint.sh --def ...   Up             3306/tcp, 33060/tcp   
```

## Return Code
Code | Meaning
---|---
0 | Success
1 | `Invalid Docker Command` or `Invalid Operation`
2 | `Invalid Docker Compose Yaml file`
98 | Parsing error for Parameters or Options
99 | Else exceptional case

<!-- ## Parameter setting examples (diagrams)
![Parameter setting examples - 1](README-image2021-12-13_10-1-9.png) -->
