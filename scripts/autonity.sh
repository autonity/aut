# Functions to starting and stopping and Autonity node

# The repository to download Autonity from If AUTONITY_VERSION is set,
# a binary release is downloaded.  If AUTONITY_BRANCH is set, the
# repository is built.  AUTONITY_TOKEN is used for authentication if
# provided.  See autonity_install.

AUTONITY_REPO=clearmatics/autonity-internal
# AUTONITY_VERSION=
AUTONITY_BRANCH=autonity-devmode

AUTONITY_KEYSTORE=../tests/data #
AUTONITY_HTTP_PORT=6066

RPC_ENDPOINT=http://localhost:${AUTONITY_HTTP_PORT}

OWNER_KEYFILE=${AUTONITY_KEYSTORE}/UTC--2022-12-01T13-20-59.210299618Z--56b25a4ded9ce76d1d4f704a97d309838f4b9dc1
OWNER_ADDR=0x56b25a4ded9ce76d1d4f704a97d309838f4b9dc1

# Build from a branch of the autonity-internal repo.  Set AUTONITY to
# point to the binary.
#
# Arguments:
# 1 - branch name
function autonity_build_from_branch() {
    # TODO: ideally this would just download a binary.

    pushd ..

        # Clone / checkout and enter the autonity directory.
        if ! [ -d autonity ] ; then
            # Determine the URL.  If we have a github token, use it.
            if ! [ "" == "${AUTONITY_TOKEN}" ] ; then
                repo_url=https://${AUTONITY_TOKEN}:x-oauth-basic@github.com/${AUTONITY_REPO}
            else
                repo_url=https://github.com/${AUTONITY_REPO}
            fi

            git clone --depth 1 --recurse-submodule --shallow-submodules -b $1 ${repo_url} autonity
            pushd autonity
        else
            pushd autonity
            git fetch --update-shallow $1
            git checkout $1
        fi

        # Build
        make all
        export AUTONITY=`pwd`/build/bin/autonity
        popd  # autonity

    popd  # ..
}

# Download and unpack a release of autonity, given a version string.
#
# Arguments:
# 1 - version string
function autonity_download_release() {
    # TODO: fix this

    AUTONITY_DOWNLOAD_URL=https://github.com/autonity/autonity-sim/releases/download/${AUTONITY_VERSION}/autonity-linux-amd64-${AUTONITY_VERSION}.tar.gz

    if ! [ -e ${AUTONITY} ] ; then
        if [ "" == "${AUTH_TOKEN}" ] ; then
            curl --fail -o autonity.tar.gz ${AUTONITY_DOWNNLOAD_URL}
        else
            curl --fail -o autonity.tar.gz -H "Authorization: token ${AUTH_TOKEN}" ${AUTONITY_DOWNNLOAD_URL}
        fi
        tar xzf autonity.tar.gz
        mv autonity ${AUTONITY}
    fi

    export AUTONITY=`pwd`/autonity
}

function autonity_install() {

    if ! [ "" == "${AUTONITY_BRANCH}" ] ; then
        autonity_build_from_branch ${AUTONITY_BRANCH}
    elif ! [ "" == "${AUTONITY_VERSION}" ] ; then
        autonity_download_release ${AUTONITY_VERSION}
    else
        echo "Nether AUTONITY_BRANCH or AUTONITY_VERSION have been set."
        return 1
    fi
}

function autonity_check_install() {
    if [ "" == "${AUTONITY}" ] ; then
        echo "AUTONITY env var not set"
        return 1
    fi
    if ! [ -e ${AUTONITY} ] ; then
        echo "No autonity executable at ${AUTONITY}"
        return 1
    fi
}

function autonity_start() {
    autonity_check_install

    pid=`pidof autonity`
    if ! [ "${pid}" == "" ] ; then
        echo "Autonity process already started."
        return 0
    fi

    ${AUTONITY} \
        --dev \
        --dev.etherbase ${OWNER_ADDR} \
        --password "" \
        --keystore ${AUTONITY_KEYSTORE} \
        --http \
        --http.addr 127.0.0.1 --http.port ${AUTONITY_HTTP_PORT} \
        --http.api aut,eth,net,tendermint,txpool,web3,admin > autonity.log 2>&1 &
}

function autonity_wait() {
    while ! (aut node info --rpc-endpoint ${RPC_ENDPOINT} > /dev/null 2>&1) ; do
        echo Waiting for Autonity node ...
        sleep 1
    done
    echo Autonity node is up.
}

function autonity_stop() {
    pid=`pidof autonity`
    echo "Autonity PID: ${pid}"
    if ! [ "${pid}" == "" ] ; then
        while (kill -SIGINT ${pid} > /dev/null 2>&1) ; do
            sleep 0.5
        done
    fi
}
