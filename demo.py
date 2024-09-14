from DrissionPage import ChromiumPage, ChromiumOptions
import csv
import asyncio
from datetime import datetime  # 导入 datetime 模块

async def fetch_job_data(url, writer):
    driver = ChromiumPage()
    driver.get(url)
    lists = driver.eles('x://ul[@class="job-list-box"]/li/div/a')
    job_urls = ['https://www.zhipin.com' + li.attrs['href'] for li in lists]

    for job_url in job_urls:
        driver.get(job_url)
        
        # 添加延迟，单位为秒
        await asyncio.sleep(2)  # 这里设置为2秒，您可以根据需要调整

        job_name_element = driver.ele('x://div[@class="name"]/h1')
        job_name = job_name_element.text if job_name_element else ''
        company_name_element = driver.ele('x://*[@id="main"]/div[3]/div/div[1]/div[2]/div/a[2]')
        company_name = company_name_element.text if company_name_element else ''
        company_address_element = driver.ele('x://*[@id="main"]/div[1]/div/div/div[1]/p/a')
        company_address = company_address_element.text if company_address_element else ''
        company_intro_element = driver.ele('x://*[@id="main"]/div[3]/div/div[2]/div[4]/div[1]/div')
        company_intro = company_intro_element.text if company_intro_element else ''
        
        # 获取当前时间戳
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 写入数据，包括时间戳
        writer.writerow([timestamp, job_name_element.text if job_name_element else '', company_name, company_address, company_intro])
        print(f'爬取完成：{timestamp} - {job_name_element.text if job_name_element else "无职位名"}')

async def main():
    co = ChromiumOptions().headless()
    writer = csv.writer(open('python爬虫.csv', mode='w', newline='', encoding='utf-8-sig'))
    writer.writerow(['时间戳', '职位名称', '公司名称', '公司地址', '公司介绍'])  # 修改表头，避免重复

    urls = [f'https://www.zhipin.com/web/geek/job?query=python%E7%88%AC%E8%99%AB&city=100010000&page={page_num}' for page_num in range(1, 6)]
    tasks = [fetch_job_data(url, writer) for url in urls]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
