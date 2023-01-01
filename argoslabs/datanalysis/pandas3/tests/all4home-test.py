import sys
# from tkinter import *
# import tkinter.filedialog
import pandas as pd
import numpy as np

# 신규 하자처리 확인서 경로 받아오기
# def Load():
#     global filename
#     filename = tkinter.filedialog.askopenfilename(initialdir="C:/Users/Myeongkook "
#                                                              "Park/Desktop/올포홈/pandas/jupylab/Scripts",
#                                                   title="신규 하자처리확인서 업로드",
#                                                   filetypes=(("xls file", "*.xls"), ("all files", "*.*")))


################################################################################
def do_job(work_fn, orig_fn, comp_fn):
    dfs = list()

    # 신규 하자처리 접수 리스트
    _df = pd.read_excel(work_fn, dtype={'LH담당자연락처': str, '하자접수일': str, '보수지시일': str, '처리기한': str})
    dfs.append(_df)

    _df = pd.read_excel(orig_fn, header=1)
    dfs.append(_df)

    # 작업 완료처리된 리스트
    _df = pd.read_excel(comp_fn, header=1)
    dfs.append(_df)

    section = '경북2권역' if work_fn.find('세음') > 0 else '경북3권역'

    # 특정 컬럼값 Null 초기화
    dfs[0]['견적금액'] = np.nan
    dfs[0]['공사금액'] = np.nan

    # 작업 리스트, 신규리스트 비교병합(중복제거)
    merge_1 = (pd.concat([dfs[1], dfs[0]], ignore_index=False, sort=False).drop_duplicates(['접수일련번호'], keep='first'))

    # 중복제거된 신규리스트만 생성
    drop_1 = (pd.concat([merge_1, dfs[1]], ignore_index=False, sort=False).drop_duplicates(['접수일련번호'], keep=False))

    # 1차 중복제거된 리스트, 완료 리스트 비교병합(중복제거)
    merge_2 = (pd.concat([dfs[2], drop_1], ignore_index=False, sort=False).drop_duplicates(['접수일련번호'], keep='first'))

    # 1,2차 중복제거 완료된 리스트
    df = (pd.concat([merge_2, dfs[2]], ignore_index=False, sort=False).drop_duplicates(['접수일련번호'], keep=False))

    df['현장담당'] = '김정'
    df['권역구분'] = np.nan

    # 2권역 매핑 배열
    section2_arr0 = ['경북혁신2', '경북혁신3', '고령다산1', '고령다산2', '고령다산3', '구미구평', '구미도량2-3', '구미도산', '구미옥계1', '구미옥계2', '구미인의', '구미황상3', '군위서부', '김천대신', '김천덕곡', '김천부곡2', '의성상리', '경북혁신']
    section2_arr1 = ['고령덕경인터빌', '구미고아에덴', '김천일천푸른마을']
    section2_arr2 = ['구미화성파크드림', '고령디오팰리스']

    # 3권역 매핑 배열
    section3_arr0 = ['경산백천', '경산사동휴먼시아1', '경산사동휴먼시아2', '경산상방', '경산진량휴먼시아', '경주건천', '경주금장', '경주안강', '경주외동', '경주용강', '영천망정5', '영천문내', '영천야사4', '청도범곡휴먼시아']
    section3_arr1 = ['경산삼주봉황1차', '경산삼주봉황2차', '경산초원장미', '경주안강에덴', '경주안강장미마을', '경주우성한빛1차', '경주우성한빛2차', '경주위덕삼성', '경주일천푸른마을', '경주전원홈그린', '한동그린타운', '한동화성타운']
    section3_arr2 = ['경산진량우림필유', '영천해피포유']

    # 실제로 사용되는 컬럼형태로 재가공
    df = df[['접수일련번호', '하자접수일', '하자진행상태', '하자구분', '하자상세구분', '단지 및 동주소', '임대유형', '대분류', '동', '호', '공간', '대표공종', '중분류', '소분류', '세분류', '하자내용', '계약번호', '견적금액', '공사금액', '민원인', '연락처', '연락처2', 'LH담당자', 'LH담당자연락처', '처리내용', '완료보고일', '보수완료일', '반려자명', '반려일', '반려사유', '보수지시일', '처리기한', '경과일', '비고', '작업자', '현장담당', '권역구분']]

    # 가구 권역구분 [2,3권역]
    if section == '경북2권역':
        df.loc[df['단지 및 동주소'].isin(section2_arr0), ['권역구분']] = '2건설'
        df.loc[df['단지 및 동주소'].isin(section2_arr1), ['권역구분']] = '2부도'
        df.loc[df['단지 및 동주소'].isin(section2_arr2), ['권역구분']] = '2리츠'
        df.loc[df['권역구분'].isnull(), ['권역구분']] = '2다가구'
    elif section == '경북3권역':
        df.loc[df['단지 및 동주소'].isin(section3_arr0), ['권역구분']] = '3건설'
        df.loc[df['단지 및 동주소'].isin(section3_arr1), ['권역구분']] = '3부도'
        df.loc[df['단지 및 동주소'].isin(section3_arr2), ['권역구분']] = '3리츠'
        df.loc[df['권역구분'].isnull(), ['권역구분']] = '3다가구'
    # 보수업체 조건
    if section == '경북2권역':
        df['비고'] = '㈜세음건설'
    elif section == '경북3권역':
        df['비고'] = '㈜이두건설'
    # else:
    #     raise ReferenceError(f'Invalid section "{section}"')

    # 엑셀로 내보내기
    df.to_csv('result-manual.csv', header=0, index=False)


################################################################################
if __name__ == '__main__':
    _work_fn = 'new.xls'
    _orig_fn = 'original.xlsm'
    _comp_fn = 'complete.xlsx'
    do_job(_work_fn, _orig_fn, _comp_fn)

