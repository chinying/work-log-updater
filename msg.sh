REPO_PATH="" # fill in with your repo path
CUR_DIR=$(pwd)
DATE=`date +%Y-%m-%d`
cd $REPO_PATH && git log --since="3 days ago" --oneline > $CUR_DIR/logs/date-$DATE-out.txt
