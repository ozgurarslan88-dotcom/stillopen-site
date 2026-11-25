# Still Open — website

Static site. No build step. Files:
- index.html — home page (latest video + all Road Files)
- videos.js — list of every video. Add new videos at the TOP.
- roads/*.html — one Road File page per video (copy knoxville-i40.html as a template)
- style.css — shared styles

## Publish on GitHub Pages (free)
1. Create a public repo on GitHub, e.g. `stillopen-site`.
2. Upload all files in this folder (keep the `roads` folder).
3. Repo → Settings → Pages → Source: "Deploy from a branch", Branch: `main`, folder `/ (root)` → Save.
4. After a minute the site is live at https://stillopenroads.com (CNAME file is already included)

## Own domain (e.g. stillopenroads.com)
1. Buy the domain (Namecheap, Cloudflare, Porkbun…).
2. GitHub → Settings → Pages → Custom domain → type the domain → Save (this creates a CNAME file).
3. At the domain registrar, add DNS records:
   - A records for @ → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
   - CNAME record for www → <your-username>.github.io
4. Back in GitHub Pages, tick "Enforce HTTPS" once it becomes available.

## Add a new video
1. In videos.js, copy the first line, paste it above, change id / title / place / state / region.
2. Optional Road File: copy roads/knoxville-i40.html, change the text, video id and sources, then add `page:"roads/<file>.html"` to the line in videos.js.
