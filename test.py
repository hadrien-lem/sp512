from selenium import webdriver
from selenium.webdriver.support.ui import Select

def test_selenium(r):
    # SET DRIVER
    # driver = webdriver.Chrome()
    driver = webdriver.Firefox()
    driver.get('http://josselin.desmars.free.fr/work/teaching/launcher/')

    # ROCKET BUILDER
    s1 = Select(driver.find_element_by_id('stage1'))
    m1 = driver.find_element_by_id('me1')
    s2 = Select(driver.find_element_by_id('stage2'))
    m2 = driver.find_element_by_id('me2')
    s3 = Select(driver.find_element_by_id('stage3'))
    m3 = driver.find_element_by_id('me3')
    mu = driver.find_element_by_id('mu')
    build = driver.find_element_by_xpath('/html/body/div[1]/form/center/table/tbody/tr/td[1]/input')

    # LAUNCH PARAMETERS
    pad = Select(driver.find_element_by_id('lpd'))
    azi = driver.find_element_by_id('azi')
    alt = driver.find_element_by_id('alt')
    slo = driver.find_element_by_id('slo')
    mission = Select(driver.find_element_by_id('mission'))
    launch = driver.find_element_by_xpath('/html/body/div[1]/center/form/table/tbody/tr/td[1]/input')

    # TEST
    m1.clear()
    m2.clear()
    m3.clear()
    mu.clear()
    azi.clear()
    alt.clear()
    slo.clear()
    
    s1.select_by_visible_text(r['s0_prop_name'])
    m1.send_keys(r['s0_prop_mass'])
    s2.select_by_visible_text(r['s1_prop_name'])
    m2.send_keys(r['s1_prop_mass'])
    s3.select_by_visible_text(r['s2_prop_name'])
    m3.send_keys(r['s2_prop_mass'])
    mu.send_keys(r['m_u'])
    build.click()

    pad.select_by_visible_text(r['pad'])
    azi.send_keys(r['azimut'])
    alt.send_keys(r['z_inj'])
    slo.send_keys(r['slope'])
    mission.select_by_value(r['mission'])
    launch.click()
