from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import easyocr

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# chromedriver의 경로를 Service 객체를 통해 지정
s = Service('C:\\chromedriver-win64\\chromedriver.exe')
driver = webdriver.Chrome(service=s)

# driver.get("http://www.google.com")
driver.get("https://tickets.interpark.com/")

print("감시를 시작합니다.")
target_url = "https://poticket.interpark.com/Book/BookMain.asp"
url_found_message_shown = False  # 원하는 URL을 찾았다는 메시지를 표시했는지 여부

while True:
    # 현재 열린 탭/창들을 확인
    for handle in driver.window_handles:
        try:
            window_handles = driver.window_handles  # 현재 열려있는 모든 창의 핸들을 가져옵니다.
            driver.switch_to.window(window_handles[-1]) 
            
            if driver.current_url == target_url and not url_found_message_shown:
                print("찾았습니다! 원하는 URL이 열렸습니다.")
                
                # 아이프레임으로 이동
                driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmSeat']"))
                
                # 부정예매방지 문자 이미지 요소 선택
                capchaPng = driver.find_element(By.XPATH,'//*[@id="imgCaptcha"]')
                if  capchaPng.location["x"] != 0:
                    ##로직 시작
                    reader = easyocr.Reader(['en'])
                    
                    while capchaPng:
                        result = reader.readtext(capchaPng.screenshot_as_png, detail=0)
                        capchaValue = result[0].replace(' ', '').replace('5', 'S').replace('0', 'O').replace('$', 'S').replace(',', '')\
                            .replace(':', '').replace('.', '').replace('+', 'T').replace("'", '').replace('`', '')\
                            .replace('1', 'L').replace('e', 'Q').replace('3', 'S').replace('€', 'C').replace('{', '').replace('-', '')
                            
                        # 입력
                        driver.find_element(By.XPATH,'//*[@id="divRecaptcha"]/div[1]/div[3]').click()
                        chapchaText = driver.find_element(By.XPATH,'//*[@id="txtCaptcha"]')
                        chapchaText.send_keys(capchaValue)
                            
                        #입력완료 버튼 클릭
                        driver.find_element(By.XPATH,'//*[@id="divRecaptcha"]/div[1]/div[4]/a[2]').click()

                        # 입력이 잘 됐는지 확인하기
                        display = driver.find_element(By.XPATH,'//*[@id="divRecaptcha"]').is_displayed()
                    
                        # 입력 문자가 틀렸을 때 새로고침하여 다시입력
                        if display:
                            # driver.find_element(By.XPATH,'//*[@id="divRecaptcha"]/div[1]/div[1]/a[1]').click()
                            driver.find_element(By.XPATH, '//a[@class="refreshBtn"]').click()
                        else:
                            select()
                            break
    
                # url_found_message_shown = True  # 메시지를 표시했다는 플래그 설정


            # 좌석 탐색
            def select():
                # print(driver.window_handles)
                # driver.switch_to.window(driver.window_handles[-1])
                # driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeat"]'))
                
                # 좌석등급 선택
                #driver.find_element(By.XPATH,'//*[@id="GradeRow"]/td[1]/div/span[2]').click()
                
                while True:
                    # 세부 구역 선택
                    driver.find_element(By.XPATH,'//*[@id="GradeDetail"]/div/ul/li[1]/a').click()
                    
                    # # 좌석선택 아이프레임으로 이동
                    # driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeatDetail"]'))
                    
                    # # 좌석이 있으면 좌석 선택
                    # try:
                    #     driver.find_element(By.XPATH,'//*[@id="Seats"]').click()
                    #     # 결제 함수 실행
                    break
                        
                    # # 좌석이 없으면 다시 조회
                    # except:
                    #     print('******************************다시선택')
                    #     driver.switch_to.default_content()
                    #     driver.switch_to.frame(driver.find_element(By.XPATH,'//*[@id="ifrmSeat"]'))
                    #     driver.find_element(By.XPATH,'/html/body/form[1]/div/div[1]/div[3]/div/p/a/img').click()
                    #     time.sleep(1)


        except Exception as e:
            print(f"오류 발생: {e}")
            continue  # 오류가 발생한 탭을 건너뛰고 계속 진행합니다.
    
    if not url_found_message_shown:
        print("확인중..")
    time.sleep(1)  # 1초마다 확인

# 루프를 빠져나오는 코드가 없으므로 이 부분은 절대 실행되지 않습니다.
# input("Press Enter to close...")
# driver.quit()
