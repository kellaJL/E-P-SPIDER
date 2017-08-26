from GetKuaidailiIp import GetKuaiDaiLiIp
def get_ip():
    s = GetKuaiDaiLiIp()
    url = 'http://www.kuaidaili.com/free/'
    for i in range(2):
        url1=url+'/inha/'+i+'/'
        s.ParseAndGetInfo(url1)