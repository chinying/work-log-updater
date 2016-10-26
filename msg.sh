REPO_PATH="" # fill in with your repo path
CUR_DIR=$(pwd)
cd $REPO_PATH && git log --since="1 days ago" --oneline > $CUR_DIR/out.txt

