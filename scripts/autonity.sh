# Functions to starting and stopping and Autonity node

AUTONITY_DOWNNLOAD_URL=https://github.com/autonity/autonity-sim/releases/download/v0.9.0/autonity-linux-amd64-v0.9.0.tar.gz

AUTONITY=../autonity
# AUTONITY=../../autonity-internal/build/bin/autonity
AUTONITY_KEYSTORE=../tests/data #
AUTONITY_HTTP_PORT=6066

RPC_ENDPOINT=http://localhost:${AUTONITY_HTTP_PORT}

OWNER_KEYFILE=${AUTONITY_KEYSTORE}/UTC--2022-12-01T13-20-59.210299618Z--56b25a4ded9ce76d1d4f704a97d309838f4b9dc1
OWNER_ADDR=0x56b25a4ded9ce76d1d4f704a97d309838f4b9dc1

function autonity_install() {
    if ! [ -e ${AUTONITY} ] ; then
        if [ "" == "${AUTH_TOKEN}" ] ; then
            curl -o autonity.tar.gz ${AUTONITY_DOWNNLOAD_URL}
        else
            curl -o autonity.tar.gz -H "Authorization: token ${AUTH_TOKEN}" ${AUTONITY_DOWNNLOAD_URL}
        fi
        tar xzf autonity.tar.gz
        mv autonity ${AUTONITY}
    fi
}

function autonity_start() {
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
