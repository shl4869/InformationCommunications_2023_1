def crc_shift_register(data, generator):
    # data: information bits
    # generator: generator bits
    data = list(map(int, data.split()))
    generator = list(map(int,generator.split()))
    # crclen: size of crc register //자주 사용하므로 헷갈리지 않게 정의해 주었음
    # crc: CRC bits
    # codeword: <data,crc> , 초기화는 data의 값만 넣음
    crclen = len(generator)-1
    crc = [0]*crclen
    codeword = [q for q in data]
    for p in range(crclen):
        data.append(0)
    # idx = first crc index (bit to be XORed with others)
    idx = 0
    for i in range (len(data)): # data에 비트가 있을 때만 돔
        # generator에서 가장 왼쪽 bit가 1이면 crc의 가장 왼쪽 bit가 XOR연산의 항으로 사용됨
        if generator[0] == 1:   
            out = crc[idx]
        # generator의 가장 오른쪽 bit가 1이면 out과 다음 data bit를 XOR한 후 CRC의 가장 왼쪽에 저장
        # 원형 배열을 사용하기 때문에 CRC의 가장 왼쪽 원소는 다음 loop에서 CRC의 가장 오른쪽 원소가 됨
        if generator[crclen] == 1:
            crc[idx] = out^data[i]
        else:
            crc[idx] = data[i]
        # 다음 원소 탐색을 위해 인덱스를 증가시킴
        # CRC의 가장 끝 bit들은 특수적인 상황이기에 for문 밖에서 처리
        idx=(idx+1)%crclen
        # 가장 끝 원소들을 제외한 나머지 원소들을 계산
        for k in range (1,crclen):    # CRC 내부에서 한바퀴 도는 루프
            # generator가 1일 때 out bit와 XOR연산을 수행
            if (generator[k]==1):
                #print("XOR index: ",k)
                crc[idx] = crc[idx]^out
            # k와 동시에 인덱스값도 증가시켜줌
            idx=(idx+1)%crclen
        # 한 data bit가 추가될 때 crc의 계산이 모두 끝나면 원형 배열의 인덱스를 증가시켜 왼쪽으로 shift된 효과를 만들어줌
        idx=(idx+1)%crclen
    crc = print_crc(idx,crc)
    # codeword에 계산된 crc bits를 이어붙임
    for j in range(len(crc)):
        codeword.append(crc[j])
    crcstr = make_string(crc)
    codewordstr = make_string(codeword)
    return crcstr, codewordstr


def print_crc(idx,crc):
    # idx가 시작index인 원형 배열 crc를 0번부터 시작하는 일반 배열로 변경
    crcprt = [0]*len(crc)
    crclen = len(crc)
    for k in range(len(crc)):
        crcprt[k] = crc[idx]
        idx=(idx+1)%crclen
    return crcprt


def make_string(arr):
    temp=""
    for k in range(len(arr)):
        temp+=str(arr[k])+" "
    return temp


def crc_check(codeword, generator):
    # 조건에 맞게 error 여부 출력
    # error 있을 때: "An error is detected (according to CCITT-16)!"
    # error 없을 때: "An error is not detected (according to CCITT-16)!"

    # codeword: codeword bits
    # generator: generator bits
    codeword = list(map(int, codeword.split()))
    generator = list(map(int,generator.split()))
    # crclen: size of crc register //자주 사용하므로 헷갈리지 않게 정의해 주었음
    # crc: CRC bits
    crclen = len(generator)-1
    crc = [0]*crclen
    # idx = first crc index (bit to be XORed with others)
    idx = 0
    for i in range (len(codeword)): # codeword에 비트가 있을 때만 돔
        # generator에서 가장 왼쪽 bit가 1이면 crc의 가장 왼쪽 bit가 XOR연산의 항으로 사용됨
        if generator[0] == 1:   
            out = crc[idx]
        # generator의 가장 오른쪽 bit가 1이면 out과 다음 codeword bit를 XOR한 후 CRC의 가장 왼쪽에 저장
        # 원형 배열을 사용하기 때문에 CRC의 가장 왼쪽 원소는 다음 loop에서 CRC의 가장 오른쪽 원소가 됨
        if generator[crclen] == 1:
            crc[idx] = out^codeword[i]
        else:
            crc[idx] = codeword[i]
        # 다음 원소 탐색을 위해 인덱스를 증가시킴
        # CRC의 가장 끝 bit들은 특수적인 상황이기에 for문 밖에서 처리
        idx=(idx+1)%crclen
        # 가장 끝 원소들을 제외한 나머지 원소들을 계산
        for k in range (1,crclen):    # CRC 내부에서 한바퀴 도는 루프
            # generator가 1일 때 out bit와 XOR연산을 수행
            if (generator[k]==1):
                #print("XOR index: ",k)
                crc[idx] = crc[idx]^out
            # k와 동시에 인덱스값도 증가시켜줌
            idx=(idx+1)%crclen
        # 한 data bit가 추가될 때 crc의 계산이 모두 끝나면 원형 배열의 인덱스를 증가시켜 왼쪽으로 shift된 효과를 만들어줌
        idx=(idx+1)%crclen
    # crc를 원형 배열이 아닌 0번 index부터 시작하는 일반 배열로 변환
    crc = print_crc(idx,crc)
    # crc에 남은 bit가 모두 0이 되지 않으면 오류를 검출하고 리턴
    # crc에 남은 bit가 모두 0이면 오류가 없음을 출력한 뒤 리턴
    for j in crc:
        if j != 0:
            if(str(crclen)==16):
                print("An error is detected (according to CCITT-16)!")
            else:
                print("An error is detected!")
            return
    if(str(crclen)==16):
        print("An error is not detected (according to CCITT-16)!")
    else:
        print("An error is not detected!")
    return

# test 함수
def hw3_part2():
    print("[HW #3 Part II] Student ID: {} Name: {}".format("2071035", "Somin Lee"))
    mode = input("Select the mode between TX and RX (TX:1, RX:2): ")

    if mode == "1":
        data = input("Type information bits that you want to send ex) 1 0 0 1 1 0 1: ")
        generator = input("Type generator bits: ")
        crc, codeword = crc_shift_register(data,generator)
        generatorlist = list(map(int,generator.split()))
        print("\n[Result]")
        if(str(len(generatorlist)-1) == 16):
            print("CRC bits calculated by CCITT-16: ", crc)
        else:
            print("CRC bits calculated: ", crc)
        print("The complete codeword: ", codeword)
        print("Done...")

    elif mode == "2":
        codeword = input("Type the codeword that RX recieved: ex) x x x ... x x: ")
        generator = input("Type generator bits: ")
        print("\n[Result]")
        crc_check(codeword,generator)
        print("Done...")
        
    else:
        print("select 1 or 2 again.")

hw3_part2()
