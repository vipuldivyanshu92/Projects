import realmfilter
import authlogonfilter

onWriteFilters = {
    #0x00 : [authlogonfilter.process]
}

onRecvFilters = {
    #0x10 : [realmfilter.process]
}
