#!/bin/sh

dry_run='n'
if [[ $1 == '--hard' || $2 == '--hard' ]];
then
	dry_run=''
fi

target_folder='dev.herbalcell.com'
if [[ $1 == '--prod' || $2 == '--prod' ]];
then
	target_folder='herbalcell.com'
fi

# find . -name '*.pyc' -print0 | xargs -0 rm

rsync -avzi${dry_run} --no-perms --no-group --chmod=ugo=rwX --delete --include 'herbalcell/templates/***'  --include 'psd/***' --exclude 'herbalcell/static/*/*/*.zip' --exclude 'herbalcell/static/*/*/*/*.zip' --include '*/misc/thumbs' --exclude '*/thumbs' --include 'herbalcell/static/***' --include 'herbalcell/' --include 'public/' --include 'public/favicon.ico' --exclude '*' ./ username@herbalcell.com:~/${target_folder} | grep '^[^.s]'

rsync -avzi${dry_run} --size-only --no-perms --no-group --chmod=ugo=rwX --delete --exclude 'settings/local.py' --exclude '*.pyc' --exclude 'herbalcell/templates' --exclude 'herbalcell/static' --include 'herbalcell/***' --exclude '*.db' --include '.gitignore' --exclude 'views.txt' --include '*.*' --exclude '*' ./ username@herbalcell.com:~/${target_folder} | grep '^[^.s]'