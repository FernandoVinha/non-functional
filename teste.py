from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# Configuração do RPC
rpc_user = 'node'
rpc_password = 'F0dase12$'
rpc_host = '192.168.0.203'  # ou use o endereço IP real se estiver acessando remotamente
rpc_port = 8332

# Cria uma conexão RPC
try:
    rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

    # Obter informações do nó de blockchain
    blockchain_info = rpc_connection.getblockchaininfo()
    print("Informações do Blockchain:", blockchain_info)

except JSONRPCException as e:
    print("Erro na conexão RPC:", e)
except Exception as e:
    print("Ocorreu um erro:", e)
