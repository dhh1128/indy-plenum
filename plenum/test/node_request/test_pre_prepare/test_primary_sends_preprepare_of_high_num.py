import time

import pytest

from stp_core.loop.eventually import eventually
from plenum.common.request import ReqDigest
from plenum.common.messages.node_messages import PrePrepare
from plenum.server.replica import TPCStat
from plenum.server.suspicion_codes import Suspicions
from plenum.test.helper import getNodeSuspicions
from plenum.test.test_node import getNonPrimaryReplicas, getPrimaryReplica
from plenum.test import waits
from plenum.test.test_node import getNonPrimaryReplicas

instId = 0


@pytest.mark.skip(reason="SOV-555. Not implemented in replica. Add a check in "
                         "replica to check value of preprepare seq number.")
def testPrePrepareWithHighSeqNo(looper, nodeSet, propagated1):
    def chk():
        for r in getNonPrimaryReplicas(nodeSet, instId):
            nodeSuspicions = len(getNodeSuspicions(
                    r.node, Suspicions.WRONG_PPSEQ_NO.code))
            assert nodeSuspicions == 1

    def checkPreprepare(replica, viewNo, ppSeqNo, req, numOfPrePrepares):
        assert (replica.prePrepares[viewNo, ppSeqNo][0]) == \
               (req.identifier, req.reqId, req.digest)

    primary = getPrimaryReplica(nodeSet, instId)
    nonPrimaryReplicas = getNonPrimaryReplicas(nodeSet, instId)
    req = propagated1.reqDigest
    primary.doPrePrepare(req)
    timeout = waits.expectedPrePrepareTime(len(nodeSet))
    for np in nonPrimaryReplicas:
        looper.run(
                eventually(checkPreprepare, np, primary.viewNo,
                           primary.lastPrePrepareSeqNo - 1, req, 1,
                           retryWait=.5, timeout=timeout))

    newReqDigest = ReqDigest(req.identifier, req.reqId + 1, req.digest)
    incorrectPrePrepareReq = PrePrepare(instId,
                                        primary.viewNo,
                                        primary.lastPrePrepareSeqNo + 2,
                                        *newReqDigest,
                                        time.time())
    primary.send(incorrectPrePrepareReq, TPCStat.PrePrepareSent)

    timeout = waits.expectedPrePrepareTime(len(nodeSet))
    looper.run(eventually(chk, retryWait=1, timeout=timeout))
