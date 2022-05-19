
## Getting Started

### Install Node LTS and npm

Node.js LTS (v16.x):

```bash
# Using Ubuntu
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Using Debian, as root
curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
apt-get install -y nodejs
```
Install dependencies and nextjs
```bash
npm install
```

## Run the necessary microservices
Run online serving: https://github.com/martinezlucas98/uca-google/tree/online-serving/online-serving

Run index server: https://github.com/martinezlucas98/uca-google/tree/index/index#readme

## Run the frontend
Run the development server:

```bash
npm run dev
# or
yarn dev
```


Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

