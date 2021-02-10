# Creating a systemd service ([Source](https://askubuntu.com/a/919059))
1. Create a file `/etc/systemd/system/newscorpus.service`
2. Content:

```
[Unit]
Description=Newscorpus
After=docker.service

[Service]
Restart=on-failure
RestartSec=5s
User=username

Type=oneshot
RemainAfterExit=yes
StandardOutput=file:/var/log/newscorpus.log
StandardError=file:/var/log/newscorpus_error.log

WorkingDirectory=/path/to/newscorpus
ExecStart=/path/to/docker-compose/docker-compose up -d
ExecStop=/path/to/docker-compose/docker-compose down

[Install]
WantedBy=multi-user.target
```

3. Commands:
Enable the service:
- `systemctl enable newscorpus`

Then:
- `service newscorpus status`
- `service newscorpus start`
- `service newscorpus stop`
- etc.