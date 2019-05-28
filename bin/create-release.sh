#!/bin/bash

ROOT_DIR=$(git rev-parse --show-toplevel)
CUR_VERSION=$(grep version $ROOT_DIR/pyproject.toml | awk -F "=" '{print $2}' | sed 's/["\ ]//g')
LAST_COMMIT=$(git log --format=%B -n1)
LAST_COMMIT_ID=$(git log --format=%h -n1)

# Check if an argument was sent and generate the new version number
if [ -z "$1" ]; then
    echo "Please specify one of theses arguments: --major, --minor, --patch"
    exit 1
else
    case $1 in
        "--major")
            NEW_VERSION=$(python3 -c "v='$CUR_VERSION'.split('.'); v[0]=str(int(v[0]) + 1); v[1]='0'; v[2]='0'; print('.'.join(v))");;

        "--minor")
            NEW_VERSION=$(python3 -c "v='$CUR_VERSION'.split('.'); v[1]=str(int(v[1]) + 1); v[2]='0'; print('.'.join(v))");;

        "--patch")
            NEW_VERSION=$(python3 -c "v='$CUR_VERSION'.split('.'); v[2]=str(int(v[2]) + 1); print('.'.join(v))");;

        *)
            echo "Please specify one of theses arguments: --major, --minor, --patch"
            exit 1;;
    esac

    # Create short version for sphinx
    SHORT_NEW_VERSION=$(python3 -c "v='$NEW_VERSION'.split('.'); print('.'.join(v[0:2]))")

fi

# Check if the script was executed inside a virtualenv
if [ -z "$VIRTUAL_ENV" ]; then
        echo "Please retry inside a virtualenv."
        exit 1
fi

# Check if the current branch are master
if [ "$(git rev-parse --abbrev-ref HEAD)" != "master" ]; then
        echo "Please execute this script in master branch."
        exit 1
fi

# Check if the HEAD have uncommited modifications
if [ ! -z "$(git status -s)" ]; then
        echo "You have uncommited modifications. Please stash your modifications or push them."
        exit 1
fi

if [ "$LAST_COMMIT" == "Release version $CUR_VERSION 🎉" ]; then
    echo "You're trying to create a empty release..."
    exit 1
fi

revert_release() {
    echo "Huhu... a step was failed, reverting the creation of the release"
    git reset --hard $LAST_COMMIT_ID
    git tag -d "v$NEW_VERSION" ||:
    exit 1
}

#########
# Starting the process for creating the release
touch $ROOT_DIR/CHANGES.txt.new
cat <<EOF > $ROOT_DIR/CHANGES.txt.new
$NEW_VERSION
-----

  - Put here the changes of this new release

EOF

cat $ROOT_DIR/CHANGES.txt >> $ROOT_DIR/CHANGES.txt.new || revert_release
$EDITOR +4 $ROOT_DIR/CHANGES.txt.new || revert_release

mv $ROOT_DIR/CHANGES.txt.new $ROOT_DIR/CHANGES.txt || revert_release

# Update the version in all files that contain the version
sed -i -E "s/(version=')$CUR_VERSION(')/\1$NEW_VERSION\2/g" $ROOT_DIR/setup.py || revert_release
sed -i -E "s/(\"version\": \")$CUR_VERSION(\")/\1$NEW_VERSION\2/g" $ROOT_DIR/package.json || revert_release
sed -i -E "s/(version = \")$CUR_VERSION(\")/\1$NEW_VERSION\2/g" $ROOT_DIR/pyproject.toml || revert_release
sed -i -E "s/(__VERSION__ = ')$CUR_VERSION(')/\1$NEW_VERSION\2/g" $ROOT_DIR/netwark/__init__.py || revert_release

# Commit the new version
git commit -am "Release version $NEW_VERSION 🎉" || revert_release
git tag "v$NEW_VERSION" || revert_release

echo "Houray! 🎉 The new version has been created and is available under the version: $NEW_VERSION!"
echo "You can now push all pending commits and the new tag with: git push --follow-tags"