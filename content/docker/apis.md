Golang : Container Lifecycle Management

In this tutorial we look at how golang can be used to access Docker Daemon API Endpoint and manage containers.

Rerence files :

All the samples use utility functions from the file util.go.

SockerRequest is the function to make a socket call to the endpoint. In our case the endpoint uses default uri scheme of unix://localhost/.... We also need to pass method which could be GET, POST, DELETE.

func SockRequest(method, endpoint string, data interface{}) (int, []byte, error) {
        ...
}
SockRequest in turn calls sockRequestRaw function to make the actual API call.

func func sockRequestRaw(method, endpoint string, data io.Reader, ct string)
         (*http.Response, io.ReadCloser, error) {
        ...
}
List Containers

We make the GET request to unix://localhost/containers/json?all=1 to get a list of containers in the JSON format. This gets Unmarshalled into samplesutils.ResponseJSON struct and then print using samplesutils.PrettyPrint.

func ListContainers() {
        _, body, err := sampleutils.SockRequest("GET", "/containers/json?all=1", nil)
        var respJSON *sampleutils.ResponseJSON
        if err = json.Unmarshal(body, &respJSON); err != nil {
                fmt.Printf("unable to unmarshal response body: %v", err)
        }
        sampleutils.PrettyPrint(respJSON)
}
This function is called from the main() function as shown below

func main() {
        ListContainers()
}
Full Code Listing

Please refer to list_containers.go. for complete code listing of the sample.

Executing the Sample

Run the following command on the bash terminal

go run dockersamples/list_containers.go
Create a Container

To create a container we are going to pass the container name and the image name. API will call the endpoint unix://localhost//containers/create?name=[container_name]. Along with the request a confirg object is passed containing the image name and a flag to make sure container is not exited.

Call to samples.SockRequest(...)

_, body, err := sampleutils.SockRequest("POST", "/containers/create?name="+name, config)
body object returned is marshalled into sampleutils.ResponseCreateContainer

type ResponseCreateContainer struct {
        Id       string
        Warnings string
Function CreateContainer(..) Listed below encloses all these calls.

func CreateContainer(name string) {
        config := map[string]interface{}{
                "Image":     "busybox",
                "OpenStdin": true,
        }
        _, body, err := sampleutils.SockRequest("POST",
                "/containers/create?name="+name, config)
        if err != nil {
                fmt.Printf("Error %v\n", err)

        } else {
                var resp *sampleutils.ResponseCreateContainer
                if err = json.Unmarshal(body, &resp); err != nil {
                        fmt.Printf("unable to unmarshal response body: %v\n", err)
                }
                sampleutils.PrettyPrint(resp)
        }

}
Full Code Listing

Please refer to create_container.go. for complete code listing of the sample.

Executing the Sample

Run the following command on the bash terminal

go run dockersamples/create_container.go <container_name>
Start Container

In the last section we learnt how to create a container. In this section we will learn how to start a container which has already been created. Note that Create and Start are two states which are not the same.

First we get the containerId from the container name : name by calling the function samplesutils.GetContainerId(name).

Http POST request call is made by calling the function samples.SockRequest(...).

status, _, err := sampleutils.SockRequest("POST",
                        "/containers/"+containerId+"/start", nil)
status which is returned by the Http call is printed to the console. Please refer to the code list for the function.

func StartContainer(name string) {
        containerId := sampleutils.GetContainerId(name)
        fmt.Printf("startContainer :Container Id : %v", containerId)
        if containerId == "" {
                fmt.Printf("Invalid Container name %v\n", name)
        } else {
                status, _, err := sampleutils.SockRequest("POST",
                        "/containers/"+containerId+"/start", nil)
                if err != nil {
                        fmt.Printf("\nerror %v\n", err)
                } else {
                        fmt.Printf("\nStatus of the Start Request: %#v\n", status)
                }
        }
}
Full Code Listing

Please refer to start_container.go. for complete code listing of the sample.

Executing the Sample

Run the following command on the bash terminal

go run dockersamples/start_container.go <container_name>





Golang : Volume Lifecycle

In this lab we learn how to use golang to create and manage volumes in Docker.

Create a Container with a Volume

Create a Map object Config which has details about the image and volume binding path/

config := map[string]interface{}{
                "Image":     "busybox",
                "OpenStdin": true,
                "Volumes": map[string]struct{}{"/tmp": {}},
        }
Pass this object to SockRequest(..) which POSTS to the default socket endpoint.

_, body, err := sampleutils.SockRequest("POST",
        "/containers/create?name="+name, config)
Function with the complete code listing. Parameter name is the name of the container which is passed to the function

func CreateContainerWithVolume(name string) {
        config := map[string]interface{}{
                "Image":     "busybox",
                "OpenStdin": true,
                "Volumes": map[string]struct{}{"/tmp": {}},
        }
        _, body, err := sampleutils.SockRequest("POST",
                "/containers/create?name="+name, config)
        if err != nil {
                fmt.Printf("Error %v\n", err)

        } else {
                var resp *sampleutils.ResponseCreateContainer
                if err = json.Unmarshal(body, &resp); err != nil {
                        fmt.Printf("unable to unmarshal response body: %v\n", err)
                }
                sampleutils.PrettyPrint(resp)
        }
}
Call the function CreateContainerWithVolume(name string) from the main() function

func main() {
        if len(os.Args) > 1 {
                arg := os.Args[1]
                name := arg
                CreateContainerWithVolume(name)
        } else {
                fmt.Printf("Please specify container name on the command line\n")
        }
}
Execute the program

$ go run dockersamples/create_container_with_volume.go test3_vol
You can start the container and inspect the container to make sure volume got bound in the specifed path.

$ docker inspect test3_vol

[{
    "AppArmorProfile": "",
    "Args": [],
    "Config": {
        ..
        "Cmd": [
            "/bin/sh"
        ],
    "Volumes": {
        "/tmp": "/var/lib/docker/vfs/dir/ad64baef817f1..08b6584881427c29214f"
    },
    "VolumesRW": {
        "/tmp": true
    }
}
]
Create a Container with Volume Binds

In this sample we bind a directory on the host (created on the fly) with a /tmp volume mounted in the container.

Create a Map object Config which has details about the image and volume binding path/

config := map[string]interface{}{
                "Image":     "busybox",
                "Volumes":   map[string]struct{}{"/tmp": {}},
                "OpenStdin": true,
        }
Pass this object to SockRequest(..) which does a Http POST to the default socket endpoint.

_, body, err := sampleutils.SockRequest("POST",
        "/containers/create?name="+name, config)
Create a bindPath in a random Host directory and pass it while starting the Container through config object. In our case this directory is /tmp/test.yJzTpXFbfH

bindPath := sampleutils.RandomUnixTmpDirPath("test")
Please refer to util.go. for more details about RandomUnixTmpDirPath(..)

In the codeblock below notice how a Map specifying relationship between bindPath and /tmp is created. Finally samplesutil.SockRequest to start the container is called with the config.

config = map[string]interface{}{
                "Binds": []string{bindPath + ":/tmp"},
}
containerId := sampleutils.GetContainerId(name)
status, _, err = sampleutils.SockRequest("POST", "/containers/"+containerId+"/start", config)
Function with the complete code listing. Parameter name is the name of the container which is passed to the function

func CreateContainerWithVolumeBinds(name string) {
        config := map[string]interface{}{
                "Image":     "busybox",
                "Volumes":   map[string]struct{}{"/tmp": {}},
                "OpenStdin": true,
        }

        status, _, err := sampleutils.SockRequest("POST", "/containers/create?name="+name, config)
        fmt.Printf("status: %v\n", status)
        if err != nil {
                fmt.Printf("Error while creating the Container: %v\n", err)
                return
        }

        bindPath := sampleutils.RandomUnixTmpDirPath("test")
        fmt.Printf("BindPath: %v\n", bindPath)

        config = map[string]interface{}{
                "Binds": []string{bindPath + ":/tmp"},
        }
        containerId := sampleutils.GetContainerId(name)
        status, _, err = sampleutils.SockRequest("POST",
                "/containers/"+containerId+"/start", config)
        fmt.Printf("Status of the call: %v\n", status)
}
Call the function CreateContainerWithVolumeBinds(name string) from the main() function

func main() {
        if len(os.Args) > 1 {
                arg := os.Args[1]
                name := arg
                CreateContainerWithVolumeBinds(name)
        } else {
                fmt.Printf("Please specify container name on the command line\n")
        }
}
Execute the program

$ go run dockersamples/create_container_with_volume_binds.go test4_vol
Container will be up and running, inspect the container to the check the bind created.

$ docker inspect test4_vol

[{
    "AppArmorProfile": "",
    "Args": [],
    "Config": {
        ..
        "Cmd": [
            "/bin/sh"
        ],
   "Volumes": {
       "/tmp": "/tmp/test.yJzTpXFbfH"
   },
   "VolumesRW": {
       "/tmp": true
   }
}
]




Python Client Library API for Docker

In this tutorial we will learn how to use Docker Python Client Library https://github.com/docker/docker-py

Installation

Python 2.x

$ pip install docker-py
Python 3.x

$ pip3 install docker-py
Connect to Docker Dameon

from docker import client
cli = Client(base_url='unix://var/run/docker.sock')
Get List of Containers

cli.containers()
[{'Command': '/bin/bash',
  'Created': 1447062465,
  'HostConfig': {'NetworkMode': 'default'},
  'Id': '7f7e943a8a854c09e9c14fdf37bfc652844621bb4cac2f308a0a3874469c1879',
  'Image': 'ubuntu',
  'ImageID': '07f8e8c5e66084bef8f848877857537ffe1c47edd01a93af27e7161672ad0e95',
  'Labels': {},
  'Names': ['/high_kare'],
  'Ports': [],
  'Status': 'Up 4 weeks'}]
Create Container

container = cli.create_container(image='ubuntu:latest', command='/bin/sleep 30')
print(container['Id'])
0f477c47c911d022d5bfd66617b7a568763b7dbf740ba46c066ae8d824bc4421
cli.containers()
[{'Command': '/bin/bash',
  'Created': 1447062465,
  'HostConfig': {'NetworkMode': 'default'},
  'Id': '7f7e943a8a854c09e9c14fdf37bfc652844621bb4cac2f308a0a3874469c1879',
  'Image': 'ubuntu',
  'ImageID': '07f8e8c5e66084bef8f848877857537ffe1c47edd01a93af27e7161672ad0e95',
  'Labels': {},
  'Names': ['/high_kare'],
  'Ports': [],
  'Status': 'Up 4 weeks'}]
Inspect Container

cli.inspect_container('7f7e943a8a854c09e9c14fdf37bfc652844621bb4cac2f308a0a3874469c1879')['Name']
'/high_kare'
Container Commit

cli.commit('7f7e943a8a854c09e9c14fdf37bfc652844621bb4cac2f308a0a3874469c1879', repository='test/container-1',
          tag='version1')
{'Id': 'bc0bfb26f00e3c883294ac284cf259d500ce2a1a7a947423dc07b1840944ab33'}
Container Restart

container_id = '7f7e943a8a854c09e9c14fdf37bfc652844621bb4cac2f308a0a3874469c1879'
try:
  cli.restart(container_id)
except Exception as e:
    print(e)
500 Server Error: Internal Server Error ("b'Cannot restart container 7f7e943a8a854c09e9c14fdf37bfc652844621bb4cac2f308a0a3874469c1879: [2] Container does not exist: container destroyed'")
Images

Get List of images using images() method.

images = cli.images()
print(images[0])
{'Size': 15, 'Created': 1449850121, 'ParentId': '07f8e8c5e66084bef8f848877857537ffe1c47edd01a93af27e7161672ad0e95', 'VirtualSize': 188304310, 'Labels': {}, 'RepoTags': ['test/container-1:version1'], 'Id': 'bc0bfb26f00e3c883294ac284cf259d500ce2a1a7a947423dc07b1840944ab33', 'RepoDigests': []}
Inspect Image

cli.inspect_image('bc0bfb26f00e3c883294ac284cf259d500ce2a1a7a947423dc07b1840944ab33')
{'Architecture': 'amd64',
 'Author': '',
 'Comment': '',
 'Config': {'AttachStderr': False,
  'AttachStdin': False,
  'AttachStdout': False,
  'Cmd': ['/bin/bash'],
  'Domainname': '',
  'Entrypoint': None,
  'Env': None,
  'Hostname': '',
  'Image': '',
  'Labels': {},
  'OnBuild': None,
  'OpenStdin': False,
  'StdinOnce': False,
  'Tty': False,
  'User': '',
  'Volumes': {'/volume1': {}},
  'WorkingDir': ''},
 'Container': '7f7e943a8a854c09e9c14fdf37bfc652844621bb4cac2f308a0a3874469c1879',
 'ContainerConfig': {'AttachStderr': True,
  'AttachStdin': True,
  'AttachStdout': True,
  'Cmd': ['/bin/bash'],
  'Domainname': '',
  'Entrypoint': None,
  'Env': None,
  'Hostname': '7f7e943a8a85',
  'Image': 'ubuntu',
  'Labels': {},
  'OnBuild': None,
  'OpenStdin': True,
  'StdinOnce': True,
  'StopSignal': 'SIGTERM',
  'Tty': True,
  'User': '',
  'Volumes': {'/volume1': {}},
  'WorkingDir': ''},
 'Created': '2015-12-11T16:08:41.294792143Z',
 'DockerVersion': '1.9.0',
 'GraphDriver': {'Data': None, 'Name': 'aufs'},
 'Id': 'bc0bfb26f00e3c883294ac284cf259d500ce2a1a7a947423dc07b1840944ab33',
 'Os': 'linux',
 'Parent': '07f8e8c5e66084bef8f848877857537ffe1c47edd01a93af27e7161672ad0e95',
 'RepoDigests': [],
 'RepoTags': ['test/container-1:version1'],
 'Size': 15,
 'VirtualSize': 188304310}
Volumes

Get List of Volumes

volumes = cli.volumes()
print(volumes['Volumes'][0])
{'Name': '07c473532ed7024bda91889e2467bbb1709df29e62ae0359c26cb24e2ab5e227', 'Driver': 'local', 'Mountpoint': '/var/lib/docker/volumes/07c473532ed7024bda91889e2467bbb1709df29e62ae0359c26cb24e2ab5e227/_data'}
Create Volume

volume = cli.create_volume(name='volume1', driver='local', driver_opts={})
print(volume)
{'Name': 'volume1', 'Driver': 'local', 'Mountpoint': '/var/lib/docker/volumes/volume1/_data'}
Using Volumes

This example shows how to use a Volume to create a container

container_id = cli.create_container(
    'busybox', 'ls', volumes=['/var/lib/docker/volumes/volume1'],
    host_config=cli.create_host_config(binds=[
        '/var/lib/docker/volumes/volume1:/mnt/vol1',
    ])
)
print(container_id)
{'Id': '31a297f9bb8c6c08a1ebd22469177f290b22a298fce103689dfc92fa88dba070', 'Warnings': None}
Inspect Volumes

cli.inspect_volume('volume1')
{'Driver': 'local',
 'Mountpoint': '/var/lib/docker/volumes/volume1/_data',
 'Name': 'volume1'}
Get Archive

ctnr = cli.create_container('ubuntu', 'true')
strm, stat = cli.get_archive(ctnr, '/bin/sh')
print(stat)
{'name': 'sh', 'linkTarget': '/bin/dash', 'size': 4, 'mode': 134218239, 'mtime': '2014-02-19T04:13:5


