import torch
import torch.nn.functional as F
import torch_geometric.utils as U
from torch.nn import Sequential as Seq, Linear as Lin, ReLU, Parameter, ModuleList
from torch_scatter import scatter_mean, scatter_max, scatter_add
from torch_geometric.nn import MetaLayer

from torch_geometric.nn.conv import GATv2Conv, TransformerConv

class GTrans_block(torch.nn.Module):
    def __init__(self,node_in,edge_in,global_in,hid,node_out,edge_out,global_out):
        super(GTrans_block, self).__init__()
        self.edge_mlp = Lin(node_in + edge_in, edge_out)
        self.node_mlp = Lin(node_in, node_out)
        self.node_model = TransformerConv(in_channels=node_in, out_channels=node_out, heads=3, edge_dim=edge_out)
        self.node_mlp_2 = Lin(node_out*4 + global_in, node_out)
        self.global_mlp = Lin(global_in + node_out, global_out)

        def edge_model(src, dest, edge_attr, glob, batch):
            out = torch.cat([src, edge_attr], 1)
            return F.relu(self.edge_mlp(out))

        def node_model(x, edge_index, edge_attr, glob, batch):
            feat = self.node_mlp(x)
            out = self.node_model(x,edge_index,edge_attr)
            out = torch.cat([feat, out, glob[batch]], dim=1)
            return F.relu(self.node_mlp_2(out))


        def global_model(x, edge_index, edge_attr, glob, batch):
            out = torch.cat([glob, scatter_mean(x, batch, dim=0)], dim=1)
            return F.relu(self.global_mlp(out))

        self.op = MetaLayer(edge_model, node_model, global_model)

    def forward(self, x, edge_index, edge_attr, glob, batch):
        return self.op(x, edge_index, edge_attr, glob, batch)

class GATv3_block(torch.nn.Module):
    def __init__(self,node_in,edge_in,global_in,hid,node_out,edge_out,global_out):
        super(GATv3_block, self).__init__()
        self.edge_mlp = Lin(node_in + edge_in, edge_out)
        self.node_model = GATv2Conv(in_channels=node_in, out_channels=node_out, heads=3, edge_dim=edge_out)
        self.node_mlp_2 = Lin(node_out*3 + global_in, node_out)
        self.global_mlp = Lin(global_in + node_out, global_out)

        def edge_model(src, dest, edge_attr, glob, batch):
            out = torch.cat([src, edge_attr], 1)
            return F.relu(self.edge_mlp(out))

        def node_model(x, edge_index, edge_attr, glob, batch):
            out = self.node_model(x,edge_index,edge_attr)
            out = torch.cat([out, glob[batch]], dim=1)
            return F.relu(self.node_mlp_2(out))

        def global_model(x, edge_index, edge_attr, glob, batch):
            out = torch.cat([glob, scatter_mean(x, batch, dim=0)], dim=1)
            return F.relu(self.global_mlp(out))

        self.op = MetaLayer(edge_model, node_model, global_model)

    def forward(self, x, edge_index, edge_attr, glob, batch):
        return self.op(x, edge_index, edge_attr, glob, batch)

class GN_block(torch.nn.Module):
    def __init__(self,node_in,edge_in,global_in,hid,node_out,edge_out,global_out):
        super(GN_block, self).__init__()
        self.edge_mlp = Lin(node_in + edge_in, edge_out)
        self.node_mlp = Lin(node_in + edge_out, node_out)
        self.node_mlp_2 = Lin(node_out + global_in, node_out)
        self.global_mlp = Lin(global_in + node_out, global_out)

        def edge_model(src, dest, edge_attr, glob, batch):
            out = torch.cat([src, edge_attr], 1)
            return F.relu(self.edge_mlp(out))

        def node_model(x, edge_index, edge_attr, glob, batch):
            row, col = edge_index
            out = torch.cat([x[col], edge_attr], dim=1)
            out = self.node_mlp(out)
            out = scatter_max(out, row, dim=0, dim_size=x.size(0))[0]
            out = torch.cat([out, glob[batch]], dim=1)
            return F.relu(self.node_mlp_2(out))

        def global_model(x, edge_index, edge_attr, glob, batch):
            out = torch.cat([glob, scatter_mean(x, batch, dim=0)], dim=1)
            return F.relu(self.global_mlp(out))

        self.op = MetaLayer(edge_model, node_model, global_model)

    def forward(self, x, edge_index, edge_attr, glob, batch):
        return self.op(x, edge_index, edge_attr, glob, batch)

class GATv2_block(torch.nn.Module):
    def __init__(self,node_in,edge_in,global_in,hid,node_out,edge_out,global_out):
        super(GATv2_block, self).__init__()
        self.edge_mlp = Lin(node_in + edge_in, edge_out)
        
        self.lin_edge = Lin(2*node_in+edge_out, node_out)
        self.node_mlp = Lin(node_in, node_out)
        self.node_mlp_2 = Lin(node_out + global_in, node_out)
        
        self.global_mlp = Lin(global_in + node_out, global_out)
        
        
        
        self.a = Parameter(torch.Tensor(1,node_out))
	
        def edge_model(src, dest, edge_attr, glob, batch):
            out = torch.cat([src, edge_attr], 1)
            return F.relu(self.edge_mlp(out))

        def node_model(x, edge_index, edge_attr, glob, batch):
            
            L,R = edge_index
                       
            leaky = self.lin_edge(torch.cat([x[L],x[R],edge_attr],dim=1))
            
            leaky = F.leaky_relu(leaky,0.2)
                        
            alpha = (leaky * self.a).sum(dim=-1)
            alpha = U.softmax(alpha, R)
            
            nodes = self.node_mlp(x) 
                        
            out = scatter_add(nodes[R]*alpha.unsqueeze(-1), R, dim=0, dim_size=x.size(0))
            
            out = torch.cat([out, glob[batch]], dim=1)
            return F.relu(self.node_mlp_2(out))
            
        def global_model(x, edge_index, edge_attr, glob, batch):
            out = torch.cat([glob, scatter_mean(x, batch, dim=0)], dim=1)
            return F.relu(self.global_mlp(out))

        self.op = MetaLayer(edge_model, node_model, global_model)

    def forward(self, x, edge_index, edge_attr, glob, batch):
        return self.op(x, edge_index, edge_attr, glob, batch)


class GNAT_block(torch.nn.Module):
    def __init__(self,node_in,edge_in,global_in,hid,node_out,edge_out,global_out):
        super(GNAT_block, self).__init__()
        self.edge_mlp = Lin(node_in + edge_in, edge_out)
        self.code = Lin(edge_out, node_out)
        self.key = Lin(node_in, node_out)
        self.node_mlp = Lin(node_in, node_out)
        self.node_mlp_2 = Lin(2*node_out + global_in, node_out)
        self.global_mlp = Lin(global_in + node_out, global_out)

        def edge_model(src, dest, edge_attr, glob, batch):
            out = torch.cat([src, edge_attr], 1)
            return F.relu(self.edge_mlp(out))

        def node_model(x, edge_index, edge_attr, glob, batch):
            S, R = edge_index
            feat = self.node_mlp(x)
            key = self.key(x)
            code = self.code(edge_attr)
            logits = (key[R]*code).sum(dim=1)
            attention = U.softmax(logits,R)
            out = scatter_add(edge_attr*attention.view(-1,1), R, dim=0, dim_size=x.size(0))
            out = torch.cat([feat, out, glob[batch]], dim=1)
            return F.relu(self.node_mlp_2(out))

        def global_model(x, edge_index, edge_attr, glob, batch):
            out = torch.cat([glob, scatter_mean(x, batch, dim=0)], dim=1)
            return F.relu(self.global_mlp(out))

        self.op = MetaLayer(edge_model, node_model, global_model)

    def forward(self, x, edge_index, edge_attr, glob, batch):
        return self.op(x, edge_index, edge_attr, glob, batch)
    



class Actions_block(torch.nn.Module):
    def __init__(self,glob_in,node_in,edge_in,hid, n_history):
        super(Actions_block, self).__init__()
        self.hid = hid
        self.glob_mlp = Lin(hid + glob_in//(2 + n_history), hid)
        self.node_mlp = Lin(hid + (node_in-1)//(2 + n_history), hid)
        self.edge_mlp2 = Lin(2*hid, hid)
        self.edge_mlp1 = Lin(2*hid + (edge_in-1)//(2 + n_history),hid)
        self.policy = Lin(hid,1)
        
    def norm(self,tensor,dev):
        l = [int(x) for x in list(tensor)]
        lnew = []
        for j in range(len(l)):
            if j==0:
                lnew.append(l[j])
            else:
                if l[j-1] == l[j]:
                    lnew.append(lnew[-1])
                else:
                    lnew.append(lnew[-1]+1)
        return torch.tensor(lnew).to(dev)
        
    def forward(self, globs, nodes, edges, G):
        row, col = G.edge_index

        actions = torch.zeros(G.num_effects.sum(),self.hid).to(globs.device)

        if G.action_globs.shape[0] > 0:
            actions[G.UA,0:self.hid] = self.glob_mlp(torch.cat([globs[G.U], G.action_globs],dim=1))
        if G.action_nodes.shape[0] > 0:
            actions[G.VA,0:self.hid] = self.node_mlp(torch.cat([nodes[G.V], G.action_nodes],dim=1))
        if G.action_edges.shape[0] > 0:
            EE = self.edge_mlp1(torch.cat([nodes[row[G.E]],G.action_edges,nodes[col[G.E]]],dim=1))
            actions[G.EA,0:self.hid] = self.edge_mlp2(torch.cat([edges[G.E], EE],dim=1))

        actions = scatter_add(actions, self.norm(G.actions_batch,globs.device), dim=0)

        return self.policy(actions)



class ACNet(torch.nn.Module):
    def __init__(self, node_in, edge_in, global_in, hid, n_history, use_attention):

        super(ACNet, self).__init__()
        self.scale = 10.0
        self.use_attention = use_attention
        
        if use_attention == '0':
            self.gn1 = GN_block(node_in,edge_in,global_in,hid,hid,hid,hid)
        elif use_attention == '1' or use_attention == '5' or use_attention == '6' :
            self.gn1 = GNAT_block(node_in,edge_in,global_in,hid,hid,hid,hid)
        elif use_attention == '2':
            self.gn1 = GATv2_block(node_in,edge_in,global_in,hid,hid,hid,hid)
        elif use_attention == '3':
            self.gn1 = GATv3_block(node_in,edge_in,global_in,hid,hid,hid,hid)
        elif use_attention == '4':
            self.gn1 = GTrans_block(node_in,edge_in,global_in,hid,hid,hid,hid) 
        
        if use_attention == '5':
            self.gn2 = GNAT_block(hid,hid,hid,hid,hid,hid,hid)
            self.gn3 = GN_block(hid,hid,hid,hid,hid,hid,hid)
        if use_attention == '6':
            self.gn2 = GNAT_block(hid,hid,hid,hid,hid,hid,hid)
            self.gn3 = GNAT_block(hid,hid,hid,hid,hid,hid,hid)
            self.gn4 = GN_block(hid,hid,hid,hid,hid,hid,hid)
        if use_attention == '7':
            self.gn1 = GTrans_block(node_in,edge_in,global_in,hid,hid,hid,hid) 
            self.gn2 = GTrans_block(hid,hid,hid,hid,hid,hid,hid)
            self.gn3 = GTrans_block(hid,hid,hid,hid,hid,hid,hid)
            self.gn4 = GTrans_block(hid,hid,hid,hid,hid,hid,hid)

        else:
            self.gn2 = GN_block(hid,hid,hid,hid,hid,hid,hid)
        
        self.policy = Actions_block(global_in,node_in,edge_in,hid, n_history)
        self.value = Seq(Lin(hid,hid), ReLU(), Lin(hid,1))

    def forward(self, g):
        nodes, edges, globs = g.x, g.edge_attr, g.glob
                
        nodes, edges, globs = self.gn1(nodes, g.edge_index, edges, globs, g.batch)
        sum_nodes = nodes; sum_edges = edges; sum_globs = globs
                
        nodes, edges, globs = self.gn2(sum_nodes, g.edge_index, sum_edges, sum_globs, g.batch)
        sum_nodes = sum_nodes + nodes; sum_edges = sum_edges + edges; sum_globs = sum_globs + globs
        
        if self.use_attention == '5':
            nodes, edges, globs = self.gn3(sum_nodes, g.edge_index, sum_edges, sum_globs, g.batch)
            sum_nodes = sum_nodes + nodes; sum_edges = sum_edges + edges; sum_globs = sum_globs + globs
        if self.use_attention == '6' or self.use_attention == '7':
            nodes, edges, globs = self.gn3(sum_nodes, g.edge_index, sum_edges, sum_globs, g.batch)
            sum_nodes = sum_nodes + nodes; sum_edges = sum_edges + edges; sum_globs = sum_globs + globs
            nodes, edges, globs = self.gn4(sum_nodes, g.edge_index, sum_edges, sum_globs, g.batch)
            sum_nodes = sum_nodes + nodes; sum_edges = sum_edges + edges; sum_globs = sum_globs + globs
        pi = self.policy(sum_globs, sum_nodes, sum_edges, g)
        
        
        pi = torch.tanh(pi)*self.scale

        val = torch.sigmoid(self.value(sum_globs))
        return pi, val
    
