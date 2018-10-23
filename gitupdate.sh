#!/bin/bash

# Revert to prior commit
# git push -f origin HEAD^:master

export git='/volume1/@appstore/git/bin/git'

$git add .
$git status
#ansible-vault encrypt .*.conf *.conf secrets.yaml entity_registry.yaml .config_entries.json .uuid
echo -n "Enter the Description for the Change: " [Minor Update] 
read CHANGE_MSG
$git commit -m "${CHANGE_MSG}"
$git push origin master
#ansible-vault decrypt .*.conf *.conf secrets.yaml entity_registry.yaml .config_entries.json .uuid

exit
