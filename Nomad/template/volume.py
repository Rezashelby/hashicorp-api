import json


def nomad_volume_payload(volume_id, volume_name, namespace):
    nomad_payload = {
        "Volumes": [
            {
                "ID": volume_id,
                "Name": volume_name,
                "Namespace": namespace,
                "PluginID": "rocket-nfs",
                "MountOptions": {
                    "FsType": "ext4",
                    "MountFlags": [
                        "rw",  # Read-Write access
                        "noatime",  # Do not update file access times on read
                        "nosuid",  # Do not allow set-user-identifier or set-group-identifier bits
                        "nodev",  # Do not interpret character or block special devices on the file system
                        # "ro",  # Mounts the file system in read-only mode
                        # "sync",  # Ensures that changes are written to the storage device immediately rather than being cached
                        # "async",  # Allows changes to be cached and written to the storage device at a later time
                        # "relatime",  # Updates the access time attribute only if the previous access time is older than the modification time
                        # "dirsync"  # Directory updates (such as creating, deleting, or renaming files) are synchronized immediately to the storage device
                    ],
                },
                "RequestedCapacityMin": 524288000,  # 500 MB
                "RequestedCapacityMax": 5368709120,  # 5 GB
                "RequestedCapabilities": [
                    {
                        "AccessMode": "multi-node-multi-writer",
                        "AttachmentMode": "file-system",
                    },
                    {
                        "AccessMode": "single-node-writer",
                        "AttachmentMode": "file-system",
                    },
                ],
            }
        ]
    }
    print(json.dumps(nomad_payload, indent=4))
    return nomad_payload


payload = nomad_volume_payload("vol-1234", "my-volume", "default")
