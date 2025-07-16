rm -rf dist ../backend/static/web ../backend/templates/index.html
npm run build
mkdir -p ../backend/static/web
cp -r dist/* ../backend/static/web
mv ../backend/static/web/index.html ../backend/templates/index.html