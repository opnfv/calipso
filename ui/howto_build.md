# Calipso

## Run

```bash                        
./run.sh
```

## Build
  
```bash
meteor build --architecture=os.linux.x86_64 ./
```
  
### Soruce Build

```bash
tar --exclude='./.meteor/local' --exclude='./node_modules' --exclude='./.git' -zcvf ../calipso-source-$(date +%Y-%m-%d).tar.gz .
```
## Testing - Build with Docker 
  
Testing on staging

```bash
docker run -d \
    -e ROOT_URL=http://testing-server-example.com \
    -e MONGO_URL=mongodb://testing-server-example.com:27017/calipso \
    -v /home/ofir/calipso:/bundle \
    -p 80:80 \
    kadirahq/meteord:base
```

Testing on local

```bash
docker run \
   --net=host \
   -e ROOT_URL=http://localhost \
   -e MONGO_URL=mongodb://localhost:27017/calipso \
   -v /home/eyal_work/projects/cisco/output:/bundle \
   kadirahq/meteord:base
```

