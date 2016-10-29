REPO_PATH="" # fill in with your repo path
CUR_DIR=$(pwd)
DATE=`date +%Y-%m-%d`
cd $REPO_PATH && git log --since="1 day ago" --pretty=format:'%h %ad %s (%an)' --date=short > $CUR_DIR/logs/date-$DATE-out.txt
