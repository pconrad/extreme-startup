# Extreme Startup

>If you are developing the project and want to see how to run it locally, scroll to the end

If you are simply wanting to play Extreme (Re)Startup, go to https://extreme-startup.fly.dev/. Hopefully it's up when you navigate to it!

### Docker

Run this if you just want to run it locally. This will 99.99% work if you have
[Docker installed](https://docs.docker.com/engine/install/)

Recommended (one command):

```
docker compose up --build
```

Shortcut using Makefile:

```
make run
```

Stop everything with:

```
docker compose down
```

Makefile shortcuts:

```
make stop
make logs
make ps
make clean
```

In this setup, the app is configured with `MONGO_URL=mongodb://mongo:27017`.

Legacy manual flow:

```
docker build -t extremestartup .
docker network create extremestartup-net
docker run -d --name mongo --network extremestartup-net -p27017:27017 mongo:7
docker run -it --rm --network extremestartup-net -p80:80 extremestartup
```
The server should be live on localhost.

When finished, clean up the MongoDB container with:

```
docker rm -f mongo
```

### Dokku

If MongoDB is provisioned separately in Dokku, configure this app to use it via
`MONGO_URL`:

```
dokku config:set <your-app-name> MONGO_URL=<your-mongodb-connection-url>
```

Connection order is:
1. `MONGO_URL` environment variable
2. `flaskr/mongo_config.json`
3. local fallback (`localhost:27017` then `mongo:27017`)

### Fork maintenance playbook

Use this if this repository stays as a long-lived fork and upstream PRs may or may not be accepted.

#### 1) Configure upstream once

```
git remote add upstream https://github.com/minutehour/extreme-startup.git
git remote -v
```

#### 2) Keep local master in sync with upstream

```
git checkout master
git fetch upstream
git rebase upstream/master
git push origin master
```

#### 3) Create and maintain a deployment branch in your fork

```
git checkout -b deploy/dokku
git push -u origin deploy/dokku
```

When upstream changes land later, refresh deploy branch from updated master:

```
git checkout deploy/dokku
git rebase master
git push --force-with-lease origin deploy/dokku
```

#### 4) Promote tested work into deploy branch

If a feature branch is ready:

```
git checkout deploy/dokku
git merge --no-ff <feature-branch>
git push origin deploy/dokku
```

If you only want selected commits:

```
git checkout deploy/dokku
git cherry-pick <commit-sha>
git push origin deploy/dokku
```

#### 5) Resolve conflicts safely during rebase

```
git status
git add <resolved-files>
git rebase --continue
```

If a rebase goes wrong:

```
git rebase --abort
```

#### 6) Recommended branch policy

1. Keep master tracking upstream as closely as possible.
2. Keep deploy/dokku as your production-ready branch.
3. Keep feature branches short-lived and PR-focused.
4. Merge to deploy/dokku only after local Docker and Dokku validation.

### Manual
Run this if you don't want to install Docker

Make sure there is a MongoDB daemon running on 27017.

```
# Starting from project root folder
# Build static files
cd frontend
npm ci
npm run build
mv dist ../flaskr/vite

# Launch flask server
cd ..
python3 -m venv env
source env/bin/activate
pip install -r flaskr/requirements.txt
flask --app flaskr --debug run
```
The server should be live on localhost:5000

## Developer guide
To see instant changes to both front and backend, follow this guide.
##### Terminal 1 - Flask server
This launches the Flask backend on **localhost:5000**. When deploying, you should have built the frontend stuff and this server would immediately serve it, but this takes an eternity, so we don't do it here. This server will **only** serve /api requests for your frontend. You can watch this terminal for any requests the frontend sends to the backend.
```
python3 -m venv env
source env/bin/activate
pip install -r flaskr/requirements.txt
flask --app flaskr --debug run
```
##### Terminal 2
WARNING: If you use WSL, make sure the project is in the Linux file directory, not the Windows one. Otherwise it doesn't live update for some reason.

This launches the React app on **localhost:5173**, which lets you see the UI updates as soon as you edit the source. Its interactions with the API on port 5000 should work.
```
cd frontend
npm ci  // Note - this needs to be ran only when new packages are added
npm run dev
```
