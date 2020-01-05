#!/bin/bash

# script to initiate after manual update of the 5 calipso containers

my_ip=$(ip route get 8.8.8.8 | head -1 | cut -d' ' -f7)
echo "running from ip:" $(my_ip)

# update local calipso code
cd /home/calipso/Calipso
git pull

# run old calipso containers using new calipso installer
# python3 /home/calipso/Calipso/base/install/calipso-installer.py --command start-all --copy q

# commit code changes to new images
echo "committing code changes..."
sleep 1
docker commit calipso-test korenlev/calipso:test-v2
docker commit calipso-monitor korenlev/calipso:monitor-v2
docker commit calipso-scan korenlev/calipso:scan-v2
docker commit calipso-api korenlev/calipso:api-v2
docker commit calipso-listen korenlev/calipso:listen-v2

# push new images to dockerhub
echo "pushing to dockerhub..."
sleep 1
docker push korenlev/calipso:test-v2
docker push korenlev/calipso:monitor-v2
docker push korenlev/calipso:scan-v2
docker push korenlev/calipso:api-v2
docker push korenlev/calipso:listen-v2

# kill and remove running containers using new calipso-installer
echo "killing running containers..."
sleep 1
python3 /home/calipso/Calipso/base/install/calipso-installer.py --command stop-all

# remove new local images
echo "removing new local images..."
sleep 1
docker rmi -f korenlev/calipso:test-v2
docker rmi -f korenlev/calipso:monitor-v2
docker rmi -f korenlev/calipso:scan-v2
docker rmi -f korenlev/calipso:api-v2
docker rmi -f korenlev/calipso:listen-v2

# pull for new images from dockerhub
echo "pulling new remote images from dockerhub..."
sleep 1
docker pull korenlev/calipso:test-v2
docker pull korenlev/calipso:monitor-v2
docker pull korenlev/calipso:scan-v2
docker pull korenlev/calipso:api-v2
docker pull korenlev/calipso:listen-v2

# remove old local untagged images
echo "removing old local images..."
sleep 5
docker rmi -f $(sudo docker images --filter 'dangling=true' -q --no-trunc)

# tag new images for cisco docker repo
echo "tagging for cisco docker repo..."
sleep 1
docker tag korenlev/calipso:test-v2 cloud-docker.cisco.com/calipso:test-v2
docker tag korenlev/calipso:monitor-v2 cloud-docker.cisco.com/calipso:monitor-v2
docker tag korenlev/calipso:scan-v2 cloud-docker.cisco.com/calipso:scan-v2
docker tag korenlev/calipso:api-v2 cloud-docker.cisco.com/calipso:api-v2
docker tag korenlev/calipso:listen-v2 cloud-docker.cisco.com/calipso:listen-v2

# push new images to cisco docker repo
echo "pushing to cisco docker repo..."
sleep 1
docker push cloud-docker.cisco.com/calipso:test-v2
docker push cloud-docker.cisco.com/calipso:monitor-v2
docker push cloud-docker.cisco.com/calipso:scan-v2
docker push cloud-docker.cisco.com/calipso:api-v2
docker push cloud-docker.cisco.com/calipso:listen-v2

exit
