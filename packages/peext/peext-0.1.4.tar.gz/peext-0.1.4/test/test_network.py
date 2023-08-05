from peext.scenario.network import create_small_test_multinet
import peext.network as network


def test_from_pandapipes():
    # GIVEN
    test_network = create_small_test_multinet()

    # WHEN
    me_network = network.from_panda_multinet(test_network)

    # THEN
    assert len(me_network.nodes) == 10
    assert len(me_network.edges) == 9
    assert len(me_network.nodes[8].edges) == 3
    assert me_network.nodes[8].edges['power'][0][1] == 'to'
    assert me_network.nodes[8].edges['power'][0][0]._id == 1
    assert me_network.nodes[8].edges['gas'][0][1] == 'to'
    assert me_network.nodes[8].edges['gas'][0][0]._id == 1
    assert me_network.nodes[8].edges['heat'][0][1] == 'from'
    assert me_network.nodes[8].edges['heat'][0][0]._id == 0
    
