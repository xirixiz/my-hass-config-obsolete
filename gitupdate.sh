#!/bin/bash

# Revert to prior commit
# git push -f origin HEAD^:master

export git='/volume1/@appstore/git/bin/git'
chmod 400 /var/services/homes/xirixiz/.ssh/id_rsa

$git add .
$git status
#ansible-vault encrypt .*.conf *.conf secrets.yaml entity_registry.yaml .config_entries.json .uuid
echo -n "Enter the Description for the Change: " [Minor Update] 
read CHANGE_MSG
$git commit -m "${CHANGE_MSG}"
$git push origin master
#ansible-vault decrypt .*.conf *.conf secrets.yaml entity_registry.yaml .config_entries.json .uuid

chmod 444 /var/services/homes/xirixiz/.ssh/id_rsa

exit
