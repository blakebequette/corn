        '''

        Modifications by blakebequette@protonmail.com
        7 December 2021

        '''


        self.log.info("Have node 1 mine another block")

        self.nodes[2].disconnect_p2ps()
        self.disconnect_nodes(1,2)
        peer_messaging = self.nodes[1].add_p2p_connection(BaseNode())

        new_block = create_block(self.tip, create_coinbase(height+1), self.block_time)
        new_block.solve()
        new_block_msg = msg_block(new_block)
        peer_messaging.send_message(new_block_msg)
        self.tip = new_block.sha256
        blocks.append(self.tip)
        self.block_time += 1
        height += 1 
        self.log.info(f'Node 1 mined block: {hex(self.tip)}')
        

        self.log.info("Send block to node 2")
        self.connect_nodes(1,2)
    
        self.log.info("Verify that node 2 received the block.")
        self.nodes[1].disconnect_p2ps()
        peer_receiving = self.nodes[2].add_p2p_connection(BaseNode())

        getdata_request = msg_getdata()
        for block in blocks:
            getdata_request.inv.append(CInv(MSG_BLOCK, block))
        peer_receiving.send_message(getdata_request)

        extra_block_tester = lambda: self.tip in peer_receiving.block_receive_map.keys()
        peer_receiving.wait_until(extra_block_tester, timeout=5)
        self.log.info(f'Node 2 received the 12th block: {extra_block_tester()}')

        '''End modifications'''