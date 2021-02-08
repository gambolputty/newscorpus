# Creating a systemd service ([Source](https://askubuntu.com/a/919059))
1. Create a file `/etc/systemd/system/newscorpus.service`
2. Content:

```
[Unit]
Description=Newscorpus
After=docker.service

[Service]
User=newscorpus

Type=oneshot
RemainAfterExit=yes

WorkingDirectory=/path/to/newscorpus
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down

[Install]
WantedBy=multi-user.target
```

3. Commands:
1. `systemctl enable newscorpus`
2. `systemctl start newscorpus`

Then:
- `service newscorpus status`
- `service newscorpus start`
- `service newscorpus stop`
- etc.