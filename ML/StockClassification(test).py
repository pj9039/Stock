import glob # 경로에 대응되는 모든 파일을 쓰기위한 모듈
import os # 파일을 다루기 위한 모듈

import xlrd # 엑셀 파일을 읽기 위한 모듈
import xlwt # 엘셀 파일을 쓰기 위한 모듈

from ML.Classificate import Classi # 표준산업분류코드 분류를 위한 모듈

CashFlow = ""
jaemusangtae = ""
IncomeStatement = ""
myfile = "BankruptcyStock(test).xls" # 결과적으로 나올파일
if os.path.isfile(myfile): # 기존에 파일이 있으면
    os.remove(myfile) # 삭제
else:
    print("Error: %s file not found" % myfile) # 없으면 없다고 표시
File_List = glob.glob('../StockData(test)/*).xls') # StockData 폴더에 있는 모든 엑셀 데이터불러오기
wbk = xlwt.Workbook() # 엑셀파일을 쓸 변수
sheet = wbk.add_sheet('sheet 1', cell_overwrite_ok=True) # 시트이름을 sheet 1
## 엑셀 1행에 쓰기 단위는 원, 상장폐지된 종목은 1 안된 종목은 0 ##
CompanyNameIdx = 0
StdInduCodeIdx = 1
StdInduIdx = 2
BasisIdx = 3
OperIncomeIdx = 4
ToojaIncomeIdx = 5
JaemooIncomeIdx = 6
CashIncomeIdx =  7
CurrentAssetsIdx = 8
NonCurrentAssetsIdx = 9
CurrentLiabilitiesIdx = 10
NonCurrentLiabilitiesIdx = 11
NetIncomeIdx = 12
BankruptcyIdx = 13
sheet.write(0, CompanyNameIdx, '기업명')                     #기본정보
sheet.write(0, StdInduCodeIdx, '표준산업분류코드')           #기본정보
sheet.write(0, StdInduIdx, '표준산업분류')               #기본정보
sheet.write(0, BasisIdx, 'basis')
sheet.write(0, OperIncomeIdx, '영업활동현금흐름')           #현금흐름표
sheet.write(0, ToojaIncomeIdx, '투자활동현금흐름')           #현금흐름표
sheet.write(0, JaemooIncomeIdx, '재무활동현금흐름')           #현금흐름표
sheet.write(0, CashIncomeIdx, '현금및현금성자산의순증가')   #현금흐름표
sheet.write(0, CurrentAssetsIdx, '유동자산')                   #재무상태
sheet.write(0, NonCurrentAssetsIdx, '비유동자산')                   #재무상태
sheet.write(0, CurrentLiabilitiesIdx, '유동부채')                   #재무상태
sheet.write(0, NonCurrentLiabilitiesIdx, '비유동부채')                   #재무상태
sheet.write(0, NetIncomeIdx, '당기/포괄순이익')           #손익계산서
#sheet.write(0, 11, '영업이익(손실)')           #손익계산서
sheet.write(0, BankruptcyIdx, '상장폐지여부')
cnt = 1 # 행
for filelist in File_List:

    wb = xlrd.open_workbook(filelist) # 엑셀 파일 오픈
    ws = wb.sheet_by_index(0) # 불러온 엑셀 파일의 첫번째 시트
    print(filelist)
    sheet_names = wb.sheet_names()
    # 시트이름이 현금흐름표/재무상태/손익계산서인 것을 찾는다
    for i in sheet_names:
        if('현금흐름표' in i):           #현금흐름표시트 찾기
            CashFlow = i
        if ('재무상태' in i or '대차대조' in i):            #재무상태표시트 찾기
            jaemusangtae = i
        if ('손익계산서' in i):          #손익계산서시트 찾기
            IncomeStatement = i
        #elif ('포괄손익계산서' in i):
        #    IncomeStatement = i
    try:
        ws1 = wb.sheet_by_name(CashFlow)            # 현금흐름표시트를 저장하는 변수
        ws2 = wb.sheet_by_name(jaemusangtae)        # 재무상태표시트를 저장하는 변수
        ws3 = wb.sheet_by_name(IncomeStatement)     # 손익계산서시트를 저장하는 변수
    except:
        sheet.write(cnt, CurrentAssetsIdx, "0")
        sheet.write(cnt, CurrentLiabilitiesIdx, "0")
        sheet.write(cnt, NonCurrentAssetsIdx, "0")
        sheet.write(cnt, NonCurrentLiabilitiesIdx, "0")
        pass
    # 첫번째 시트(기본정보)의 최대 행과 열
    ncol = ws.ncols
    nlow = ws.nrows
    # 선택 시트(현금흐름표)의 최대 행과 열
    ncol1 = ws1.ncols
    nlow1 = ws1.nrows
    ncol2 = ws2.ncols
    nlow2 = ws2.nrows
    ncol3 = ws3.ncols
    nlow3 = ws3.nrows
    # 종목명을 입력하기위해 파일이름을 쓰는데 확장자와 년도를 빼는 작업
    stockname = filelist.replace('.xls', '')
    stockname = stockname.replace('(2015)','')
    stockname = stockname.replace('(2014)','')
    stockname = stockname.replace('(2013)','')
    stockname = stockname.replace('(2012)','')
    stockname = stockname.replace('(2011)', '')
    stockname = stockname.replace('(2010)', '')
    stockname = stockname.replace('(2009)', '')
    stockname = stockname.replace('../StockData(test)\\', '')
    sheet.write(cnt, CompanyNameIdx, stockname) # 종목명을 1열에 입력한다.

    # 엑셀파일마다 형식이 달라서 2행1열의 부분이 '문서정보'인 것과 '기 본 정 보'인 파일을 나누어서 표준산업분류코드를 찾는다.
    if (ws.row_values(1)[0] == '문서정보'):
        i = 0
        j = 0
        # 최대 행길이 까지 루프
        while i < nlow:
            if("표준산업분류코드" in ws.row_values(i)[0]):
                code = (ws.row_values(i)[0]).split()[2].strip()
                Classi(code,sheet,cnt)
                sheet.write(cnt, StdInduCodeIdx , code)
            i += 1
    if (ws.row_values(3)[0] == '기 본 정 보'):
        i = 0
        while i < nlow:
            if (ws.row_values(i)[0].strip() == '표준산업분류코드'):
                code = (ws.row_values(i)[1].strip())
                Classi(code, sheet, cnt)
                sheet.write(cnt, StdInduCodeIdx , code)
            i += 1

    i=0
    # 현금흐름표의 최대 행까지 루프
    print(nlow1)
    while i < nlow1:
        tmp = ws1.row_values(i)[0].replace(" ", "") # 영업활동 현금 흐름 처럼 띄어쓰기되어있는것을 띄어쓰기 제거

        # 영업활동현금흐름 부분을 찾고 기록
        if ("영업활동현금흐름" in tmp or "영업활동으로인한현금흐름" in tmp or "영업에서창출된현금흐름" in tmp):
            OperIncome = ws1.row_values(i)[1]
            try:
                sheet.write(cnt, OperIncomeIdx , OperIncome)
            except:
                pass
        # 투자활동현금흐름 부분을 찾고 기록
        elif ("투자활동현금흐름" in tmp or "투자활동으로인한현금흐름" in tmp or "투자에서창출된현금흐름" in tmp):
            ToojaIncome = ws1.row_values(i)[1]
            try:
                sheet.write(cnt, ToojaIncomeIdx , ToojaIncome)
            except:
                pass
        # 재무활동현금흐름 부분을 찾고 기록
        elif ("재무활동현금흐름" in tmp or "재무활동으로인한현금흐름" in tmp or "재무에서창출된현금흐름" in tmp):
            JaemooIncome = ws1.row_values(i)[1]
            try:
                sheet.write(cnt, JaemooIncomeIdx , JaemooIncome)
            except:
                pass
        # 현금및현금성자산의순증가 부분을 찾고 기록
        elif ("현금및현금성자산의순증가" in tmp or "현금및현금성자산의순증감" in tmp or "현금의증가" in tmp or "현금및현금성자산의증가" in tmp or "현금및현금성자산의증감" in tmp or "현금및현금성자산순증가" in tmp or "현금및현금성자산의감소" in tmp or "현금의감소" in tmp or "현금및현금성자산의순증가" in tmp or "현금의증가(감소)" in tmp or "현금및현금성자산의순증가(감소)" in tmp or "Ⅵ.현금의증가(감소)" in tmp or "Ⅴ.현금의증가(감소)" in tmp):
            CashIncome = ws1.row_values(i)[1]
            try:
                sheet.write(cnt, CashIncomeIdx , CashIncome)
            except:

                pass

        i += 1

    j=0
    ###################재무상태
    while j < nlow2:
        tmp = ws2.row_values(j)[0].replace(" ", "") # 영업활동 현금 흐름 처럼 띄어쓰기되어있는것을 띄어쓰기 제거
        # 영업활동현금흐름 부분을 찾고 기록
        if ("유동자산" == tmp or "Ⅰ.유동자산" == tmp):
            CurrentAssets = ws2.row_values(j)[1]
            try:
                sheet.write(cnt, CurrentAssetsIdx , CurrentAssets)
            except:
                pass
        elif ("비유동자산" == tmp or "Ⅲ.비유동자산" == tmp or "Ⅱ.비유동자산" == tmp):
            NonCurrentAssets = ws2.row_values(j)[1]
            try:
                sheet.write(cnt, NonCurrentAssetsIdx , NonCurrentAssets)
            except:
                pass

        elif ("유동부채" == tmp or "Ⅰ.유동부채" == tmp):
            CurrentLiabilities = ws2.row_values(j)[1]
            try:
                sheet.write(cnt, CurrentLiabilitiesIdx , CurrentLiabilities)
            except:
                pass

        elif ("비유동부채" == tmp or "Ⅱ.비유동부채" == tmp):
            NonCurrentLiabilities = ws2.row_values(j)[1]
            try:
                sheet.write(cnt, NonCurrentLiabilitiesIdx , NonCurrentLiabilities)
            except:
                pass

        j += 1

    j=0
    ###################손익계산서
    while j < nlow3:
        tmp = ws3.row_values(j)[0].replace(" ", "")  # 영업활동 현금 흐름 처럼 띄어쓰기되어있는것을 띄어쓰기 제거
        # 당기순이익/포괄순이익 부분을 찾고 기록
        if ("당기순이익(손실)" in tmp or "Ⅷ.당기순이익(손실)" == tmp or "Ⅷ.총포괄손익" == tmp or "XII.총포괄손실" == tmp or "XⅢ.총포괄손익" == tmp or "총포괄순이익(손실)" == tmp or "총포괄이익(손실)" == tmp or "총포괄손익" == tmp or "당기총포괄이익" == tmp or "당기총포괄손익" == tmp or "연결당기총포괄(손)익" == tmp):
            NetIncome = ws3.row_values(j)[1]
            try:
                sheet.write(cnt, NetIncomeIdx , NetIncome)
            except:
                pass
        j += 1

    try:
        sheet.write(cnt, BankruptcyIdx , "1") # StockData폴더에 있는 종목들은 다 상장폐지된 종목이기 때문에 상장폐지가 되었다는 의미로 1를 입력
        sheet.write(cnt, BasisIdx , "1")
    except:
        pass
    cnt = cnt+1

File_List1 = glob.glob('../StockData(notest)/*.xls') # StockData 폴더에 있는 모든 엑셀 데이터불러오기
for filelist in File_List1:
    wb = xlrd.open_workbook(filelist) # 엑셀 파일 오픈
    ws = wb.sheet_by_index(0) # 불러온 엑셀 파일의 첫번째 시트
    print(filelist)
    sheet_names = wb.sheet_names()
    # 시트이름이 현금흐름표인것을 찾는다
    for i in sheet_names:
        if ('현금흐름표' in i):
            CashFlow = i
        if ('재무상태' in i or '대차대조' in i):
            jaemusangtae = i
        if ('손익계산서' in i):          #손익계산서시트 찾기
            IncomeStatement = i
        #elif ('포괄손익계산서' in i):
        #    IncomeStatement = i
    try:
        ws1 = wb.sheet_by_name(CashFlow) # 현금흐름표시트를 저장하는 변수
        ws2 = wb.sheet_by_name(jaemusangtae) # 재무상태표시트를 저장하는 변수
        ws3 = wb.sheet_by_name(IncomeStatement)     # 손익계산서시트를 저장하는 변수

    except:
        sheet.write(cnt, CurrentAssetsIdx , "0")
        sheet.write(cnt, CurrentLiabilitiesIdx , "0")
        sheet.write(cnt, NonCurrentAssetsIdx, "0")
        sheet.write(cnt, NonCurrentLiabilitiesIdx, "0")
        pass
    # 첫번째 시트(기본정보)의 최대 행과 열
    ncol = ws.ncols
    nlow = ws.nrows
    # 선택 시트(현금흐름표)의 최대 행과 열
    ncol1 = ws1.ncols
    nlow1 = ws1.nrows
    ncol2 = ws2.ncols
    nlow2 = ws2.nrows
    ncol3 = ws3.ncols
    nlow3 = ws3.nrows
    # 종목명을 입력하기위해 파일이름을 쓰는데 확장자와 년도를 빼는 작업
    stockname = filelist.replace('.xls', '')
    stockname = stockname.replace('(2015)','')
    stockname = stockname.replace('(2014)','')
    stockname = stockname.replace('(2013)','')
    stockname = stockname.replace('(2012)','')
    stockname = stockname.replace('(2011)', '')
    stockname = stockname.replace('(2010)', '')
    stockname = stockname.replace('(2009)', '')
    stockname = stockname.replace('../StockData(notest)\\', '')
    sheet.write(cnt, CompanyNameIdx , stockname) # 종목명을 1열에 입력한다.

    # 엑셀파일마다 형식이 달라서 2행1열의 부분이 '문서정보'인 것과 '기 본 정 보'인 파일을 나누어서 표준산업분류코드를 찾는다.
    if (ws.row_values(1)[0] == '문서정보'):
        i = 0
        # 최대 행길이 까지 루프
        while i < nlow:
            if("표준산업분류코드" in ws.row_values(i)[0]):
                code = (ws.row_values(i)[0]).split()[2].strip()
                Classi(code,sheet,cnt)
                sheet.write(cnt, StdInduCodeIdx , code)
            i += 1
    if (ws.row_values(3)[0] == '기 본 정 보'):
        i = 0
        while i < nlow:
            if (ws.row_values(i)[0].strip() == '표준산업분류코드'):
                code = (ws.row_values(i)[1].strip())
                Classi(code, sheet, cnt)
                sheet.write(cnt, StdInduCodeIdx , code)
            i += 1
    i=0
    # 현금흐름표의 최대 행까지 루프
    while i < nlow1:
        tmp = ws1.row_values(i)[0].replace(" ", "") # 영업활동 현금 흐름 처럼 띄어쓰기되어있는것을 띄어쓰기 제거

        # 영업활동현금흐름 부분을 찾고 기록
        if ("영업활동현금흐름" in tmp or "영업활동으로인한현금흐름" in tmp or "영업에서창출된현금흐름" in tmp):
            OperIncome = ws1.row_values(i)[1]
            try:
                sheet.write(cnt, OperIncomeIdx , OperIncome)
            except:
                pass
        # 투자활동현금흐름 부분을 찾고 기록
        elif ("투자활동현금흐름" in tmp or "투자활동으로인한현금흐름" in tmp or "투자에서창출된현금흐름" in tmp):
            ToojaIncome = ws1.row_values(i)[1]
            try:
                sheet.write(cnt, ToojaIncomeIdx , ToojaIncome)
            except:
                pass
        # 재무활동현금흐름 부분을 찾고 기록
        elif ("재무활동현금흐름" in tmp or "재무활동으로인한현금흐름" in tmp or "재무에서창출된현금흐름" in tmp):
            JaemooIncome = ws1.row_values(i)[1]
            try:
                sheet.write(cnt, JaemooIncomeIdx , JaemooIncome)
            except:
                pass
        # 현금및현금성자산의순증가 부분을 찾고 기록
        elif ("현금및현금성자산의순증가" in tmp or "현금및현금성자산의순증감" in tmp or "현금의증가" in tmp or "현금및현금성자산의증가" in tmp or "현금및현금성자산의증감" in tmp or "현금및현금성자산순증가" in tmp or "현금및현금성자산의감소" in tmp or "현금의감소" in tmp or "현금및현금성자산의순증가" in tmp or "현금의증가(감소)" in tmp or "현금및현금성자산의순증가(감소)" in tmp or "Ⅵ.현금의증가(감소)" in tmp or "Ⅴ.현금의증가(감소)" in tmp or "Ⅵ.현금의증가(감소)" in tmp):
            CashIncome = ws1.row_values(i)[1]
            try:
                sheet.write(cnt, CashIncomeIdx , CashIncome)
            except:
                pass
        i += 1

    j=0
    ###################재무상태
    while j < nlow2:
        tmp = ws2.row_values(j)[0].replace(" ", "") # 영업활동 현금 흐름 처럼 띄어쓰기되어있는것을 띄어쓰기 제거
        # 영업활동현금흐름 부분을 찾고 기록
        if ("유동자산" == tmp or "Ⅰ.유동자산" == tmp):
            CurrentAssets = ws2.row_values(j)[1]
            try:
                sheet.write(cnt, CurrentAssetsIdx , CurrentAssets)
            except:
                pass
        elif ("비유동자산" == tmp or "Ⅲ.비유동자산" == tmp or "Ⅱ.비유동자산" == tmp):
            NonCurrentAssets = ws2.row_values(j)[1]
            try:
                sheet.write(cnt, NonCurrentAssetsIdx , NonCurrentAssets)
            except:
                pass

        elif ("유동부채" == tmp or "Ⅰ.유동부채" == tmp):
            CurrentLiabilities = ws2.row_values(j)[1]
            try:
                sheet.write(cnt, CurrentLiabilitiesIdx , CurrentLiabilities)
            except:
                pass

        elif ("비유동부채" == tmp or "Ⅱ.비유동부채" == tmp):
            NonCurrentLiabilities = ws2.row_values(j)[1]
            try:
                sheet.write(cnt, NonCurrentLiabilitiesIdx , NonCurrentLiabilities)
            except:
                pass
        j += 1

    j=0
    ###################손익계산서
    while j < nlow3:
        tmp = ws3.row_values(j)[0].replace(" ", "")  # 영업활동 현금 흐름 처럼 띄어쓰기되어있는것을 띄어쓰기 제거
        # 당기순이익/포괄순이익 부분을 찾고 기록
        if ("당기순이익(손실)" == tmp or "Ⅷ.당기순이익(손실)" == tmp or "Ⅷ.총포괄손익" == tmp or "XII.총포괄손실" == tmp or "XⅢ.총포괄손익" == tmp or "총포괄순이익(손실)" == tmp or "총포괄이익(손실)" == tmp or "총포괄손익" == tmp or "당기총포괄이익" == tmp or "당기총포괄손익" == tmp or "연결당기총포괄(손)익" == tmp or "Ⅹ.당기순이익(손실)" == tmp or "XIV.당기순이익(손실)" == tmp or "XⅡ.당기순이익(손실)" == tmp):
            NetIncome = ws3.row_values(j)[1]
            try:
                sheet.write(cnt, NetIncomeIdx , NetIncome)
            except:
                pass

        j += 1

    try:
        sheet.write(cnt, BankruptcyIdx , "0") # StockData폴더에 있는 종목들은 다 상장폐지된 종목이기 때문에 상장폐지가 되었다는 의미로 1를 입력
        sheet.write(cnt, BasisIdx , "1")

    except:
        pass
    cnt = cnt+1
wbk.save('BankruptcyStock(test).xls') # 지금까지 쓴 엑셀데이터 저장