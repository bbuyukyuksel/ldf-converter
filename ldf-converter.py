#!/usr/bin/env python3
#-*-coding: utf-8 -*-

#########################################
#########################################
###  yazar  : burakbüyükyüksel        ###
###  e-mail : bbuyukyuksel@gmail.com  ###
###  tarih  : 15.09.2018              ###
#########################################
#########################################

import sys, json
uidnumber = 1001;

nereden = "OU=Kullanici,OU=Sehir,OU=Bolum,OU=Tasra,OU=NET,DC=NET,DC=GOV,DC=TR"
nereye = "ou=Ankara,ou=Tasra,ou=Kullanıcılar,dc=site,dc=gov,dc=tr"

domain = "domain"
guid = "guid"

loginShell = "loginShell: /bin/bash\n"
homeDirectory_fmt = "homeDirectory: /home/{}/{}"
uidnumber_fmt = "uidnumber: {}\n"

cur_state = 0
states = 5


def start_progress():
    global guid, domain, uidnumber
    print("\033[01;33m ")
    print("{} : {}".format("Nereden", nereden))
    print("{} : {}".format("Nereye", nereye))
    print("{} : {}".format("domain", domain))
    print("{} : {}".format("guid", guid))
    print("\033[00m")

    _guidNumber = "guidNumber: {}\n".format(str(guid))

    try:
        with open("ExportUser.ldif", "r") as fout :
            print("#Progress is started")
            with open ("ImportUser.ldif", "w") as fin:
                for line in fout:
                    if nereden in line:
                        line = line.replace(nereden,nereye)

                    if "objectClass: user" in line:
                        line = line.replace("user", "posixAccount")

                    if "cn" in line:
                        line_sn_copy = line.replace("cn", "sn")
                        fin.write(line)
                        fin.write(line_sn_copy)
                        continue

                    if "givenName" in line:
                        continue

                    if "sAMAccountName" in line:
                        line = line.replace("sAMAccountName", "uid")
                        uid_info = line.split(" ")
                        fin.write(line)

                        #HomeDirectory
                        homeDirectory = homeDirectory_fmt.format(domain, uid_info[1])
                        fin.write(homeDirectory)

                        #loginShell
                        fin.write(loginShell)

                        #uidnumber
                        _uidnumber = uidnumber_fmt.format(str(uidnumber))
                        uidnumber += 1
                        fin.write(_uidnumber)

                        #guidNumber
                        fin.write(_guidNumber)
                        continue

                    if "userPrincipalName" in line:
                        #line = line.replace("userPrincipalName", "mail")
                        continue

                    fin.write(line)
    except:
        print("Beklenmedik Hata:", sys.exc_info()[1])
        raise

def state_progress():
    global cur_state, states
    sure = input("\033[01;32mBilgilerinizin doğruluğundan emin misiniz? [E/h/go] : \033[00m")
    # H/h
    if (sure.lower() == "h"):
        print("\033[01;31m #Bilgilerinizi Tekrardan Giriniz \033[00m")
        return "same"
    # GO,go
    elif ("go" in sure.lower()):
    # Dallanıyor
        cmd, state_no = sure.split(":")
        state_no = int(state_no)
        if (state_no >= 0 and state_no <= states):
            cur_state = state_no
            return "other"
        else:
            print("\033[01;31m #Hatalı Adım Numarası [{}] \033[00m".format(str(state_no)))

    # E/e
    else:
        if cur_state < states:
            cur_state += 1
            return "next"
        else:
            exit()

if __name__ == "__main__":

    create_conf_file = False

    while(True):
        print("\033[01;35m #Adım[{}] \033[00m".format(str(cur_state)))
        if(cur_state == 0):
            try:
                with open("ldf-converter.conf", "r") as conf:
                    default_settings = json.load(conf)
                    nereden = default_settings["nereden"]
                    nereye = default_settings["nereye"]
                    domain = default_settings["domain"]
                    guid = default_settings["guid"]

                    print("\033[01;33m ")
                    print("{} : {}".format("Nereden", nereden))
                    print("{} : {}".format("Nereye", nereye))
                    print("{} : {}".format("domain", domain))
                    print("{} : {}".format("guid", guid))
                    print("\033[00m")


                    status = input("Yukarıdaki ayarlarla devam etmek ister misiniz? [e/H] :")
                    if status.lower() == "e" :
                        cur_state = 4
            except:
                print("\n\n\033[00;31m\t\t####\033[00m")
                print("\033[01;36m| ldf-converter conf dosyası bulunamadı!\n"
                      "|\033[00;36m işlemler bitince otomatik olarak oluşturulacak.\033[00m")
                print("\033[00;31m\t\t####\033[00m")
                create_conf_file = True

            print("\033[01;34m LDF Converter\033[00m")
            print("\033[01;37m")
            print("  + Adım[{}] -> {}".format("0", "VARSAYILAN DEĞERLERİ YÜKLE"))
            print("  + Adım[{}] -> {}".format("1", "NEREDEN"))
            print("  + Adım[{}] -> {}".format("2", "NEREYE"))
            print("  + Adım[{}] -> {}".format("3", "DOMAIN"))
            print("  + Adım[{}] -> {}".format("4", "GUID"))
            print("  + Adım[{}] -> {}".format("5", "PROGRESS"))
            print("\033[00m",end="")
            print("\033[01;32m   #Herhangi bir adıma dallanmak için \033[00;31mgo:<Adım Numarası>\033[00m\n")
            cur_state += 1

        elif(cur_state == 1):
            print("Örnek -> ", nereden)
            temp = input("Nereden taşınacak : ")
            status = state_progress()
            if(status == "next"):
                nereden = temp

        elif(cur_state == 2):
            print("Örnek -> ", nereye)
            temp = input("Nereye taşınacak : ")
            status = state_progress()
            if(status == "next"):
                nereye = temp

        elif (cur_state == 3):
            print("Örnek -> /home/",domain,sep="")
            temp = input("Domain : ")
            status = state_progress()
            if (status == "next"):
                domain = temp
        elif (cur_state == 4):
            print("Örnek -> ", guid)
            temp = input("GUID : ")
            status = state_progress()
            if (status == "next"):
                guid = temp

        elif(cur_state == 5):
            print("\033[01;31m#Progress is started.. \033[00m")
            start_progress()
            print("\033[01;31m#Progress is finished.. \033[00m")
            overwrite = True
            over_ = input("\033[01;31m#Şuan ki ayarlarınız kaydedilsin mi? [E/h] : \033[00m")
            if over_.lower() == "h":
                overwrite = False
            break


    try:
        if create_conf_file or overwrite:
            print("\033[01;36m#ldf-converter conf dosyası oluşturuluyor...\033[00m")
            default_settings = {
                "nereden": nereden,
                "nereye": nereye,
                "domain": domain,
                "guid": guid
            }
        with open("ldf-converter.conf", "w") as conf:
            json.dump(default_settings, conf, indent=4)
    except :
        print("\033[01;31m Beklenmedik Hata: \033[00m", sys.exc_info()[1])
        raise

print("\033[01;32m- END - \033[00m")