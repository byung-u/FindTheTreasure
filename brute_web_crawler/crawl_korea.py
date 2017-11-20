#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import re

from bs4 import BeautifulSoup
from datetime import datetime


class UseDataKorea:  # www.data.go.kr
    def __init__(self, bw):
        pass

    def realstate_trade(self, bw):
        now = datetime.now()
        time_str = '%4d%02d' % (now.year, now.month)

        for district_code in bw.apt_district_code:
            request_url = '%s?LAWD_CD=%s&DEAL_YMD=%s&serviceKey=%s' % (
                          bw.apt_trade_url, district_code, time_str, bw.apt_svc_key)
            self.request_realstate_trade(bw, request_url)

    def request_realstate_trade(self, bw, request_url):

        req = urllib.request.Request(request_url)
        try:
            res = urllib.request.urlopen(req)
        except UnicodeEncodeError:
            bw.logger.error('[OpenAPI] UnicodeEncodeError')
            return -1

        data = res.read().decode('utf-8')
        soup = BeautifulSoup(data, 'html.parser')
        if (soup.resultcode.string != '00'):
            bw.logger.error('[OpenAPI] %s', soup.resultmsg.string)
            return -1

        items = soup.findAll('item')
        for item in items:
            item = item.text
            item = re.sub('<.*?>', ' ', item)
            info = item.split()
            if info[3] not in bw.apt_dong:
                continue
            # if info[5].find(bw.apt_trade_apt) == -1:
            #     continue
            ret_msg = '%s %s(%sm²) %s층 %s만원 준공:%s 거래:%s년%s월%s일\n#매매' % (
                      info[3], info[4], info[7],
                      info[10], info[0], info[1],
                      info[2], info[5], info[6])

            if bw.is_already_sent('KOREA', ret_msg):
                continue
            bw.post_tweet(ret_msg, 'Realestate')

    def realstate_rent(self, bw):
        now = datetime.now()
        time_str = '%4d%02d' % (now.year, now.month)

        for district_code in bw.apt_district_code:
            request_url = '%s?LAWD_CD=%s&DEAL_YMD=%s&serviceKey=%s' % (
                          bw.apt_rent_url, district_code, time_str, bw.apt_svc_key)
            self.request_realstate_rent(bw, request_url)

    def request_realstate_rent(self, bw, request_url):
        req = urllib.request.Request(request_url)
        try:
            res = urllib.request.urlopen(req)
        except UnicodeEncodeError:
            bw.logger.error('[OpenAPI] UnicodeEncodeError')
            return -1

        data = res.read().decode('utf-8')
        soup = BeautifulSoup(data, 'html.parser')
        if (soup.resultcode.string != '00'):
            bw.logger.error('[OpenAPI] %s', soup.resultmsg.string)
            return -1

        items = soup.findAll('item')
        for item in items:
            item = item.text
            item = re.sub('<.*?>', ' ', item)
            info = item.split()
            if info[2] not in bw.apt_dong:
                continue
            # if info[5].find(bw.apt_trade_apt) == -1:
            #     continue
            ret_msg = '%s %s(%sm²) %s층 %s만원(%s) 준공:%s 거래:%s년%s월%s일\n#전월세' % (
                      info[2], info[4], info[8], info[11],
                      info[3], info[6], info[0],
                      info[1], info[5], info[7])

            if bw.is_already_sent('KOREA', ret_msg):
                continue
            bw.post_tweet(ret_msg, 'Realestate')

    def get_cha_tender(self, bw):  # 문화재청
        base_url = 'http://www.cha.go.kr'
        url = 'http://www.cha.go.kr/tenderBbz/selectTenderBbzList.do?mn=NS_01_05'
        r = bw.request_and_get(url, 'CHA')
        if r is None:
            return

        soup = BeautifulSoup(r.text, 'html.parser')
        sessions = soup.select('table > tbody > tr > td > a')
        for s in sessions:
            result_url = '%s%s' % (base_url, s['href'])
            if len(s.text.strip()) == 0:
                    continue
            if bw.is_already_sent('KOREA', s.text.strip()):
                bw.logger.info('Already sent: %s', result_url)
                continue
            short_url = bw.shortener_url(result_url)
            if short_url is None:
                short_url = result_url
            ret_msg = '%s\n%s\n#문화재청' % (s.text.strip(), short_url)
            bw.post_tweet(ret_msg, 'CHA')

    def get_cha_news(self, bw):  # 문화재청
        base_url = 'http://www.cha.go.kr'
        url = 'http://www.cha.go.kr/newsBbz/selectNewsBbzList.do?sectionId=b_sec_1&mn=NS_01_02_01'
        r = bw.request_and_get(url, 'CHA')
        if r is None:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        sessions = soup.select('table > tbody > tr > td > a')
        for s in sessions:
            result_url = '%s%s' % (base_url, s['href'])
            if len(s.text.strip()) == 0:
                    continue
            if bw.is_already_sent('KOREA', s.text.strip()):
                bw.logger.info('Already sent: %s', result_url)
                continue
            short_url = bw.shortener_url(result_url)
            if short_url is None:
                short_url = result_url
            ret_msg = '%s\n%s\n#문화재청(보도)' % (short_url, s.text.strip())
            bw.post_tweet(ret_msg, 'CHA')

        url = 'http://www.cha.go.kr/newsBbz/selectNewsBbzList.do?sectionId=b_sec_1&mn=NS_01_02_02'
        r = bw.request_and_get(url, 'CHA')
        if r is None:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        sessions = soup.select('table > tbody > tr > td > a')
        for s in sessions:
            result_url = '%s%s' % (base_url, s['href'])
            if len(s.text.strip()) == 0:
                    continue
            if bw.is_already_sent('KOREA', s.text.strip()):
                bw.logger.info('Already sent: %s', result_url)
                continue
            short_url = bw.shortener_url(result_url)
            if short_url is None:
                short_url = result_url
            ret_msg = '%s\n%s\n#문화재청(해명)' % (short_url, s.text.strip())
            bw.post_tweet(ret_msg, 'CHA')

    def get_ftc_news(self, bw):  # 공정관리위원회
        base_url = 'http://www.ftc.go.kr/news/ftc/'
        url = 'http://www.ftc.go.kr/news/ftc/reportboList.jsp'
        r = bw.request_and_get(url, 'FTC')
        if r is None:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        sessions = soup.select('table > tbody > tr > td > a')
        for s in sessions:
            result_url = '%s%s' % (base_url, s['href'])
            if len(s.text.strip()) == 0:
                    continue
            if bw.is_already_sent('KOREA', result_url):
                bw.logger.info('Already sent: %s', result_url)
                continue
            short_url = bw.shortener_url(result_url)
            if short_url is None:
                short_url = result_url
            ret_msg = '%s\n%s\n#공정위(보도)' % (short_url, s.text.strip())
            bw.post_tweet(ret_msg, 'FTC')

        url = 'http://www.ftc.go.kr/news/ftc/reportheList.jsp'
        r = bw.request_and_get(url, 'FTC')
        if r is None:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        sessions = soup.select('table > tbody > tr > td > a')
        for s in sessions:
            result_url = '%s%s' % (base_url, s['href'])
            if len(s.text.strip()) == 0:
                    continue
            if bw.is_already_sent('KOREA', result_url):
                bw.logger.info('Already sent: %s', result_url)
                continue
            short_url = bw.shortener_url(result_url)
            if short_url is None:
                short_url = result_url
            ret_msg = '%s\n%s\n#공정위(해명)' % (short_url, s.text.strip())
            bw.post_tweet(ret_msg, 'FTC')

    def get_mfds_news(self, bw):  # 식약처
        base_url = 'http://www.mfds.go.kr'
        url = 'http://www.mfds.go.kr/index.do?mid=675'
        r = bw.request_and_get(url, 'MFDS')
        if r is None:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        sessions = soup.select('table > tbody > tr > td > a')
        for s in sessions:
            result_url = '%s%s' % (base_url, s['href'])
            if len(s.text.strip()) == 0:
                    continue
            if bw.is_already_sent('KOREA', result_url):
                bw.logger.info('Already sent: %s', result_url)
                continue
            short_url = bw.shortener_url(result_url)
            if short_url is None:
                short_url = result_url
            ret_msg = '%s\n%s\n#식약처(보도)' % (short_url, s.text.strip())
            bw.post_tweet(ret_msg, 'MFDS')

        url = 'http://www.mfds.go.kr/index.do?mid=676'
        r = bw.request_and_get(url, 'MFDS')
        if r is None:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        sessions = soup.select('table > tbody > tr > td > a')
        for s in sessions:
            result_url = '%s%s' % (base_url, s['href'])
            if len(s.text.strip()) == 0:
                    continue
            if bw.is_already_sent('KOREA', result_url):
                bw.logger.info('Already sent: %s', result_url)
                continue
            short_url = bw.shortener_url(result_url)
            if short_url is None:
                short_url = result_url
            ret_msg = '%s\n%s\n#식약처(해명)' % (short_url, s.text.strip())
            bw.post_tweet(ret_msg, 'MFDS')

    def get_tta_tender(self, bw):  # 한국정보통신기술협회 입찰공고
        base_url = 'http://www.tta.or.kr/news/'
        url = 'http://www.tta.or.kr/news/tender.jsp'
        r = bw.request_and_get(url, 'TTA')
        if r is None:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        # s_container > div.scontent > div.content > table > tbody > tr:nth-child(2) > td.t_left > a
        sessions = soup.select('div > table > tbody > tr > td > a')
        for s in sessions:
            # print(s)
            result_url = '%s%s' % (base_url, s['href'])
            # print(s.text.strip(), result_url)
            if bw.is_already_sent('KOREA', result_url):
                bw.logger.info('Already sent: %s', result_url)
                continue
            short_url = bw.shortener_url(result_url)
            if short_url is None:
                short_url = result_url
            ret_msg = '%s\n%s\n#한국정보통신기술협회' % (s.text.strip(), short_url)
            ret_msg = bw.check_max_tweet_msg(ret_msg)
            bw.post_tweet(ret_msg, 'TTA')

    def get_molit_tender(self, bw):  # 국토교통부 입찰공고
        url = 'http://www.molit.go.kr/USR/tender/m_83/lst.jsp'
        r = bw.request_and_get(url, 'MOLIT')
        if r is None:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        for ll in soup.find_all('tbody'):
            for tr in ll.find_all('tr'):
                try:
                    tr.a['href']
                except TypeError:
                    continue
                href = 'http://www.molit.go.kr/USR/tender/m_83/%s' % tr.a['href'][1:]
                if bw.is_already_sent('KOREA', href):
                    bw.logger.info('Already sent: %s', href)
                    continue
                short_url = bw.shortener_url(href)
                if short_url is None:
                    short_url = href
                ret_msg = '%s\n%s\n#국토부' % (tr.a.text, short_url)
                ret_msg = bw.check_max_tweet_msg(ret_msg)
                bw.post_tweet(ret_msg, 'molit')

    def get_molit_news(self, bw):  # 국토교통부 보도자료
        url = 'http://www.molit.go.kr/USR/NEWS/m_71/lst.jsp'
        r = bw.request_and_get(url, 'MOLIT')
        if r is None:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        for tbody in soup.find_all('tbody'):
            for tr in tbody.find_all('tr'):
                try:
                    tr.a['href']
                except TypeError:
                    continue
                href = 'http://www.molit.go.kr/USR/NEWS/m_71/%s' % tr.a['href']
                if bw.is_already_sent('KOREA', href):
                    bw.logger.info('Already sent: %s', href)
                    continue
                short_url = bw.shortener_url(href)
                if short_url is None:
                    short_url = href
                ret_msg = '%s\n%s\n#국토부' % (short_url, tr.a.text)
                ret_msg = bw.check_max_tweet_msg(ret_msg)
                bw.post_tweet(ret_msg, 'molit')

    def get_mss_noti(self, bw):  # 중소벤처기업부
        url = 'http://www.mss.go.kr/site/smba/ex/bbs/List.do?cbIdx=81'
        r = bw.request_and_get(url, 'MSS')
        if r is None:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        sessions = soup.select('table > tbody > tr > td > a')
        for s in sessions:
            if s.get('onclick') is None:
                continue
            idx = s.get('onclick').replace("'", '').split(',')[1]
            result_url = 'http://www.mss.go.kr/site/smba/ex/bbs/View.do?cbIdx=81&bcIdx=%s&parentSeqa%s' % (idx, idx)

            if bw.is_already_sent('KOREA', result_url):
                bw.logger.info('Already sent: %s', result_url)
                continue
            short_url = bw.shortener_url(result_url)
            if short_url is None:
                short_url = result_url
            ret_msg = '%s\n%s\n#중소벤처기업부' % (s.text.strip(), short_url)
            bw.post_tweet(ret_msg, 'MSS')

    def get_mss_news(self, bw):  # 중소벤처기업부
        url = 'http://www.mss.go.kr/site/smba/ex/bbs/List.do?cbIdx=86'
        r = bw.request_and_get(url, 'MSS')
        if r is None:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        sessions = soup.select('table > tbody > tr > td > a')
        for s in sessions:
            if s.get('onclick') is None:
                continue
            idx = s.get('onclick').replace("'", '').split(',')[1]
            result_url = 'http://www.mss.go.kr/site/smba/ex/bbs/View.do?cbIdx=86&bcIdx=%s&parentSeq=%s' % (idx, idx)
            if bw.is_already_sent('KOREA', result_url):
                bw.logger.info('Already sent: %s', result_url)
                continue
            short_url = bw.shortener_url(result_url)
            if short_url is None:
                short_url = result_url
            ret_msg = '%s\n%s\n#중소벤처기업부(보도)' % (short_url, s.text.strip())
            bw.post_tweet(ret_msg, 'MSS')

        url = 'http://www.mss.go.kr/site/smba/ex/bbs/List.do?cbIdx=87'
        r = bw.request_and_get(url, 'MSS')
        if r is None:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        sessions = soup.select('table > tbody > tr > td > a')
        for s in sessions:
            if s.get('onclick') is None:
                continue
            idx = s.get('onclick').replace("'", '').split(',')[1]
            result_url = 'http://www.mss.go.kr/site/smba/ex/bbs/View.do?cbIdx=87&bcIdx=%s&parentSeq=%s' % (idx, idx)
            if bw.is_already_sent('KOREA', result_url):
                bw.logger.info('Already sent: %s', result_url)
                continue
            short_url = bw.shortener_url(result_url)
            if short_url is None:
                short_url = result_url
            ret_msg = '%s\n%s\n#중소벤처기업부(해명)' % (short_url, s.text.strip())
            bw.post_tweet(ret_msg, 'MSS')

    def get_kostat_news(self, bw):  # 통계청

        base_url = 'http://kostat.go.kr'
        url = 'http://kostat.go.kr/portal/korea/kor_nw/2/1/index.board'
        r = bw.request_and_get(url, 'KOSTAT')
        if r is None:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        # ct_board > fieldset > table > tbody > tr:nth-child(1) > td.title > a
        sessions = soup.select('table > tbody > tr > td > a')
        for s in sessions:
            # print(s)
            result_url = '%s%s' % (base_url, s['href'])
            if len(s.text.strip()) == 0:
                    continue
            if bw.is_already_sent('KOREA', result_url):
                bw.logger.info('Already sent: %s', result_url)
                continue
            short_url = bw.shortener_url(result_url)
            if short_url is None:
                short_url = result_url
            ret_msg = '%s\n%s\n#통계청' % (short_url, s.text.strip())
            bw.post_tweet(ret_msg, 'KOSTAT')

    def get_tta_news(self, bw):  # 한국정보통신기술협회 입찰공고
        base_url = 'http://www.tta.or.kr/news/'
        url = 'http://www.tta.or.kr/news/tender.jsp'
        r = bw.request_and_get(url, 'TTA')
        if r is None:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        # s_container > div.scontent > div.content > table > tbody > tr:nth-child(2) > td.t_left > a
        sessions = soup.select('div > table > tbody > tr > td > a')
        for sess in sessions:
            result_url = '%s%s' % (base_url, sess['href'])
            if bw.is_already_sent('KOREA', result_url):
                bw.logger.info('Already sent: %s', result_url)
                continue
            short_url = bw.shortener_url(result_url)
            if short_url is None:
                short_url = result_url
            ret_msg = '%s\n%s\n#TTA' % (short_url, sess.text.strip())
            bw.post_tweet(ret_msg, 'TTA')

    def get_visit_korea(self, bw):  # 대한민국 구석구석 행복여행
        base_url = 'http://korean.visitkorea.or.kr/kor/bz15/where/festival'
        url = 'http://korean.visitkorea.or.kr/kor/bz15/where/festival/festival.jsp'
        r = bw.request_and_get(url, 'VISIT_KOREA')
        if r is None:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        for s in soup.find_all(bw.match_soup_class(['item'])):
            if s.h3 is None:
                continue
            result_url = '%s/%s' % (base_url, s.a['href'])
            if bw.is_already_sent('KOREA', result_url):
                bw.logger.info('Already sent: %s', result_url)
                continue
            desc = repr(s.h3)[4: -6]
            for info in s.find_all(bw.match_soup_class(['info2'])):
                for span in info.find_all('span', {'class': 'date'}):
                    short_url = bw.shortener_url(result_url)
                    if short_url is None:
                        short_url = result_url
                    ret_msg = '%s\n%s\n%s\n#visitkorea' % (short_url, span.text, desc)
                    bw.post_tweet(ret_msg, 'VISIT_KOREA')
                    break
