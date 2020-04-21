# -*- coding: utf-8 -*-
from config.all_config import *


class update_caipan_close(Manager):
    name = 'update_caipan_close'

    def __init__(self):
        Manager.__init__(self, 'ysh_update_caipan_close')
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        self.get_content = re.compile(r'prepend\(unescape\("(.*?)"\)\);', re.S)
        self.get_content_1 = re.compile(r'prepend.*?unescape.*?"(.*?)"\)\);', re.S)
        self.content = re.compile('prepend\(unescape\("(.*?)"\)\);', re.S)
        self.table_text = re.compile(r'<table id=\\"cc\\" >(.*?)</table>', re.S)
        self.position_1 = re.compile(r'position (.*?)-.*?malformed', re.S)
        self.position_2 = re.compile(r'position .*?-(.*?):', re.S)
        self.str_data = re.compile(r'position .*?: malformed (.*?) character', re.S)

    def clear_html(self, s):
        data = ['.highlight{font-size:14px', 'font-family:微软雅黑', '}#addCommenttd{margin-right:20px', 'text-align:left',
                '}.comment{margin-top:5px', 'text-align:left', 'border-bottom:1pxdottedgray', 'padding-bottom:5px',
                '}.commentspan{margin-right:10px', 'font-size:12px', 'font-family:微软雅黑', '}.comcontent{background:gray',
                'height:50px', 'width:980px', 'font-family:微软雅黑', 'padding:3px0px3px10px', '}.top_ban{width:1025px',
                'height:185px', 'background:url(/Content/Head/img/tfxfy1.jpg)no-repeatleft', 'margin:0pxauto',
                '}#sddmdiv{position:absolute', 'visibility:hidden', 'top:42px',
                'background-image:url(/App_Themes/Theme09/img/tc_bg.png)', 'border-bottom:4pxsolid#0C4B9F', 'margin:0',
                'width:140px', 'padding:10px0px10px0px', 'z-index:1001', '}#sddmdiva{position:relative',
                'display:block', 'white-space:nowrap', 'line-height:30px', 'font-weight:normal', 'text-decoration:none',
                'color:#0C4B9F', 'font-size:12px', 'padding-left:10px', '}#sddmli{margin:0', 'padding:0',
                'list-style:none', 'float:left', 'line-height:38px', 'width:95px', 'position:relative', 'z-index:1001',
                '}#sddmdiva:hover{color:#fff', 'background-color:#0C4B9F', '}#sddmli.sddma:hover{height:43px',
                'color:#333', 'background:url(/App_Themes/Theme09/img/muen_1.gif)repeat-xleftbottom',
                '}.topmenubgxlqfyw{width:1024px', 'height:43px', 'line-height:25px',
                'background:url(/App_Themes/Theme09/img/muen2.gif)repeat-xleftcenter', 'margin:0pxauto', '}',
                '公告一、本裁判文书库公布的裁判文书由相关法院录入和审核，并依据法律与审判公开的原则予以公开。若有关当事人对相关信息内容有异议的，可向公布法院书面申请更正或者下镜。二、本裁判文书库提供的信息仅供查询人参考，内容以正式文本为准。非法使用裁判文书库信息给他人造成损害的，由非法使用人承担法律责任。三、本裁判文书库信息查询免费，严禁任何单位和个人利用本裁判文书库信息牟取非法利益。四、未经许可，任何商业性网站不得建立与裁判文书库及其内容的链接，不得建立本裁判文书库的镜像（包括全部和局部镜像），不得拷贝或传播本裁判文书库信息。',
                '.highlight', 'font-size:14px', 'font-family', '微软雅黑', '#addCommenttd', 'margin-right', '20px',
                'text-align', 'left', 'padding-bottom', '5px', 'addCommenttd', '1pxdottedspan', 'comcontent',
                '3pxpx3px._ban', '12url', 'Content', 'Head', 'img', 'tfxfy1', '.jpg', 'no-repeatpxauto', 'sddmdiv',
                '-image4pxsolid', 'C4B9F14pxpxpx11', 'sddmdiva', 'line-3px', 'C4B9F', 'sddmli', 'line-911',
                'sddmdivahover', 'sddmahover', 'App_Themes', 'Theme9', 'muen_1', '.gif', 'repeat-xbottom',
                'menubgxlqfyw', '124pxurl', 'App_Themes', 'Theme9', 'muen2', 'repeat-xcenterpxauto', '', '.comment',
                'margin-top', '5px', 'text-align', 'left', 'border-bottom', '1pxdottedgray',
                '公告一、本裁判文书库公布的裁判文书由相关法院录入和审核，并依据法律与审判公开的原则予以公开。若有关当事人对相关信息内容有异议的，可向公布法院书面申请更正或者下镜。二、本裁判文书库提供的信息仅供查询人参考，内容以正式文本为准。非法使用裁判文书库信息给他人造成损害的，由非法使用人承担法律责任。三、本裁判文书库信息查询免费，严禁任何单位和个人利用本裁判文书库信息牟取非法利益。四、未经许可，任何商业性网站不得建立与裁判文书库及其内容的链接，不得建立本裁判文书库的镜像（包括全部和局部镜像），不得拷贝或传播本裁判文书库信息。',
                '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '.highlight{font-size', ':',
                '14px', ';', 'font-family', ':', '微软雅黑', ';', '}#addCommenttd{margin-right', ':', '20px', ';',
                'text-align', ':', 'left', ';', '}.comment{margin-top', ':', '5px', ';', 'text-align', ':', 'left', ';',
                'border-bottom', ':', '1pxdottedgray', ';', 'padding-bottom', ':', '5px', ';',
                '}.commentspan{margin-right', ':', '10px', ';', 'font-size', ':', '12px', ';', 'font-family', ':',
                '微软雅黑', ';', '}.comcontent{background', ':', 'gray', ';', 'height', ':', '50px', ';', 'width', ':',
                '980px', ';', 'font-family', ':', '微软雅黑', ';', 'padding', ':', '3px0px3px10px', ';', '}.top_ban{width',
                ':', '1025px', ';', 'height', ':', '185px', ';', 'background', ':',
                'url(/Content/Head/img/tfxfy1.jpg)no-repeatleft', ';', 'margin', ':', '0pxauto', ';',
                '}#sddmdiv{position', ':', 'absolute', ';', 'visibility', ':', 'hidden', ';', 'top', ':', '42px', ';',
                'background-image', ':', 'url(/App_Themes/Theme09/img/tc_bg.png)', ';', 'border-bottom', ':',
                '4pxsolid#0C4B9F', ';', 'margin', ':', ';', 'width', ':', '140px', ';', 'padding', ':',
                '10px0px10px0px', ';', 'z-index', ':', ';', '}#sddmdiva{position', 'ban12url', 'relative', ';',
                'display', ':', 'block', ';', 'white-space', ':', 'nowrap', ';', 'line-height', ':', '30px', ';',
                'font-weight', ':', 'normal', ';', 'text-decoration', ':', 'none', ';', 'color', ':', '#0C4B9F', ';',
                'font-size', ':', '12px', ';', 'padding-left', ':', '10px', ';', '}#sddmli{margin', ':',
                '3pxpx3px', 'padding', ':', ';', 'list-style', ':', 'none', ';', 'float', ':', 'left', ';',
                'line-height', ':', '38px', ';', 'width', ':', '95px', ';', 'position', ':', 'relative', ';', 'z-index',
                ':', '1001', ';', '}#sddmdiva', ':', 'hover{color', ':', '#fff', ';', 'background-color', ':',
                '#0C4B9F', 'addCommenttd1pxdottedspan', '}#sddmli.sddma', ':', 'hover{height', ':', '43px', ';',
                'color', ':', '#333', ';', 'background', ':',
                'url(/App_Themes/Theme09/img/muen_1.gif)repeat-xleftbottom', ';', '}.topmenubgxlqfyw{width', ':',
                '1024px', ';', 'height', ':', '43px', ';', 'line-height', ':', '25px', ';', 'background', ':',
                'url(/App_Themes/Theme09/img/muen2.gif)repeat-xleftcenter', ';', 'margin', ':', '0pxauto', ';', '}',
                '</div><divstyle=', ':', '25pt', ';', 'TEXT-INDENT', ':', '30pt', ';', 'MARGIN', ':', '0.5pt0cm', ';',
                'FONT-FAMILY', ':', '宋体', ';', 'FONT-SIZE', ':', '15pt', ';', "'></div><divstyle='LINE-HEIGHT", ':',
                '25pt', ';', 'TEXT-INDENT', ':', '30pt', ';', 'MARGIN', ':', '0.5pt0cm', ';', 'FONT-FAMILY', ':', '宋体',
                ';', 'FONT-SIZE', ':', '15pt', ';', "'>本裁定立即执行。</div><divstyle='TEXT-ALIGN", ':', 'right', ';',
                'LINE-HEIGHT', ':', '25pt', ';', 'MARGIN', ':', '0.5pt36pt0.5pt0cm', ';', 'FONT-FAMILY', ':', '宋体', ';',
                'FONT-SIZE', ':', '15pt', ';', "'>审判员刘秋元</div><divstyle='TEXT-ALIGN", ':', 'right', ';', 'LINE-HEIGHT',
                ':', '25pt', ';', 'MARGIN', ':', '0.5pt36pt0.5pt0cm', ';', 'FONT-FAMILY', ':', '宋体', ';', 'FONT-SIZE',
                ':', '15pt', ';', "'>二〇一九年一月三日</div><divstyle='TEXT-ALIGN", ':', 'right', ';', 'LINE-HEIGHT', ':',
                '25pt', ';', 'MARGIN', ':', '0.5pt36pt0.5pt0cm', ';', 'FONT-FAMILY', ':', '宋体', ';', 'FONT-SIZE', ':',
                '15pt', ';', '>书记员胡福定</div></BODY></HTML>',
                'fot-sizefot-familyaddCommettdmagi-ighttext-alig.commetmagi-text-aligbode-bottom1pxdottedgaypaddig-bottom.commetspamagi-ightfot-sizefot-family.comcotetbackgoudgayfot-familypaddig3pxpx3px._ba1218backgoudul(/Cotet///)o-epeatmagipxautosddmdivpositiohiddebackgoud-imageul(//Theme9//tc_bg.pg)bode-bottom4pxsolidmagi14pxpaddigpxpxz-idex11sddmdivapositioelativeowaplie-3pxfot-weightomaltext-decoatiooecolofot-sizepaddig-sddmlimagipaddigoelie-9positioelativez-idex11sddmdivahovecolofffbackgoud-colosddmli.sddmahovecolo333backgoudul(//Theme9//mue_1)epeat-xbottom.meubgxlqfyw124pxlie-2backgoudul(//Theme9//mue2)epeat-xcetemagipxauto',
                """".htmvaswfpath=//++.swfvaIsCovetSwf=TuevadocText=<!DOCTYPEHTMLPUBLIC-//W3C//DTDHTML4.Tasitioal//EN'><HTML><HEAD><TITLE></TITLE></HEAD><BODY><divstyle='TEXT-ALIGNcete.5ptcm黑体18pt'>""",
                """</div><divstyle='TEXT-ALIGNcete.5ptcm黑体18pt'>""",
                """</div><divstyle='TEXT-ALIGNight.5ptcm'>""",
                """</div><divstyle='3pt.5ptcm'>""",
                """</div><divstyle='TEXT-ALIGNight.5pt36pt.5ptcm'>""",
                '''</div></BODY></HTML>if(docText.legth>1)vam=$()m.(1%)if(m.()>3)m.css(text-alig,)elseif((.legth==14||.legth==13)&&(.subst(8,2)==24||.subst(8,2)==25||.subst(8,2)==26||.subst(8,2)==27))$().html('')elsevafp=ewFlexPapeViewe('/','',cofigSwfFileescape(swfpath),Scale.6,ZoomTasitio'easeOut',ZoomTime.5,ZoomIteval.2,FitPageOLoadfalse,FitWidthOLoadtue,FullSceeAsMaxWidowfalse,PogessiveLoadigfalse,MiZoomSize.2,MaxZoomSize5,SeachMatchAllfalse,IitViewMode'Potait',PitPapeAsBitmapfalse,ViewModeToolsVisibletue,ZoomToolsVisibletue,NavToolsVisibletue,CusoToolsVisibletue,SeachToolsVisibletue,localeChai'')fuctiohtml_decode(st)vas=if(st.legth==)etus=st.eplace(/&/g,&)//2s=s.eplace(/</g,)s=s.eplace(//g,)s=s.eplace(/'/g,')s=s.eplace(/"/g,)s=s.eplace(//g,)etus.mag124pxautomagipxauto.foot1lie-39pxtext-aligcetecolofffbackgoudul(//Theme9//dow)epeat-x.wthacoloffftext-decoatiooe.wthalikcoloffftext-decoatiooe联系我们|设为首页|加入收藏Copyights©212-216AllRightsReseved.湖北省黄冈市团风县人民法院版权所有如有转载或引用本站文章涉及版权问题，请与我们联系地址黄冈市团风县人民路8号邮编438鄂ICP备121191号-1if(.()).().hef=mailtoif(.(jb_mail)).(jb_mail).hef=mailto''',
                """.htmvaswfpath=//++.swfvaIsCovetSwf=TuevadocText=<!DOCTYPEHTMLPUBLIC-//W3C//DTDHTML4.Tasitioal//EN'><HTML><HEAD><TITLE></TITLE></HEAD><BODY><divstyle='TEXT-ALIGNcete.5ptcm黑体18pt'>""",
                """fot-sizefot-familyaddCommettdmagi-ighttext-alig.commetmagi-text-aligbode-bottom1pxdottedgaypaddig-bottom.commetspamagi-ightfot-sizefot-family.comcotetbackgoudgayfot-familypaddig3pxpx3pxTabmagipxpaddigpxbode1pxsolidCBCFCE682pxTab.Meuboxfive682px32pxbackgoud-(/Cotet/mastes/ed1_2//tab_title_bg)backgoud-epeatepeat-xTab.MeuboxfiveulmagipxpaddigpxTab.Meuboxfivelicusopoite32pxpaddig-6pxcolo53ABfot-size9pxtext-aligcetebackgoud-(/Cotet/mastes/ed1_2//tab_title_bode)backgoud--epeatbackgoud-positioightTab.Meuboxfiveli.hovebackgoud-(/Cotet/mastes/ed1_2//tab_hove_bg)backgoud-positiocetebackgoud--epeatfot-sizefot-weightbold32pxcoloFFFFFFTab.CotetboxfivecleabothTabuloebodybackgoudul(/Cotet/mastes/ed1_2//page_bg)epeat-yceteFde41.meubg993px36pxmagipxautobodepxbackgoudff/*ewmeu*/sddmmagipaddigz-idex11sddmlimagipaddigoelie-33px9positioelativez-idex11sddmlihovefot-weightboldsddmli.sddmacoloffffot-sizetext-aligcetetext-decoatiooez-idex11backgoud-(/Cotet///meu_ight_b)backgoud--epeatbackgoud-positioightcetesddmli.sddmahovecoloffffot-weightboldsddmli.sddma_1coloffffot-sizetext-aligcetetext-decoatiooez-idex11sddmli.sddma_1hovecoloffffot-weightboldsddmdivpositiohiddebackgoud-(/Cotet///tc_bg.pg)bode-bottom4pxsolidffmagi14pxpaddigpxpxz-idex11sddmdivapositioelativeowaplie-3pxfot-weightomaltext-decoatiooecolo99fot-sizepaddig-sddmdivahovecolofffbackgoud-coloD532/*ewmeued*/""",
                """</div></BODY></HTML>if(docText.legth>1)vam=$()m.(1%)if(m.()>3)m.css(text-alig,)elseif((.legth==14||.legth==13)&&(.subst(8,2)==24||.subst(8,2)==25||.subst(8,2)==26||.subst(8,2)==27))$().html('')elsevafp=ewFlexPapeViewe('/','',cofigSwfFileescape(swfpath),Scale.6,ZoomTasitio'easeOut',ZoomTime.5,ZoomIteval.2,FitPageOLoadfalse,FitWidthOLoadtue,FullSceeAsMaxWidowfalse,PogessiveLoadigfalse,MiZoomSize.2,MaxZoomSize5,SeachMatchAllfalse,IitViewMode'Potait',PitPapeAsBitmapfalse,ViewModeToolsVisibletue,ZoomToolsVisibletue,NavToolsVisibletue,CusoToolsVisibletue,SeachToolsVisibletue,localeChai'')fuctiohtml_decode(st)vas=if(st.legth==)etus=st.eplace(/&/g,&)//2s=s.eplace(/</g,)s=s.eplace(//g,)s=s.eplace(/'/g,')s=s.eplace(/"/g,)s=s.eplace(//g,)etus.avfot-sizelie-33pxcolo666backgoud-coloe8e6e6text-aligcete33px1pxmagipxauto.black_wzacolo333fot-sizetext-decoatiooe.black_wzalikcolo333网站首页|新闻中心|法院介绍|审务公开|Copyights©213-215AllRightsReseved.麻城市人民法院版权所有如有转载或引用本站文章涉及版权问题，请与我们联系地址湖北省麻城市金桥大道邮编4383鄂ICP备121191号-1if(.()).().hef=mailtoif(.(jb_mail)).(jb_mail).hef=mailto""",
                """fot-sizefot-familyaddCommettdmagi-ighttext-alig.commetmagi-text-aligbode-bottom1pxdottedgaypaddig-bottom.commetspamagi-ightfot-sizefot-family.comcotetbackgoudgayfot-familypaddig3pxpx3px.233px993pxbackgoudul(/Cotet///zwqfy1)o-epeatmagipxauto.meubgbackgoud-(//Theme5//meu.pg)backgoud-epeatepeat-x/*ewmeu*/sddmmagipaddigz-idex11sddmlimagipaddigoebackgoud--epeatbackgoud-positioightcetelie-9positioelativez-idex11sddmlihovefot-weightboldsddmli.sddmacoloffffot-sizetext-aligcetetext-decoatiooez-idex11bode-ight-stylesolidbode-ight-coloFFFbode-ight-thi9sddmli.sddmahovecoloFFFfot-weightboldsddmli.sddma1coloffffot-sizetext-aligcetetext-decoatiooez-idex111pxsddmli.sddma1hovecoloFFFfot-weightboldsddmdivpositiohidde3pxbackgoud-(//Theme5//tc_bg.pg)bode-bottom4pxsolidmagi14pxpaddigpxpxz-idex11sddmdivapositioelativeowaplie-3pxfot-weightomaltext-decoatiooecolofot-sizepaddig-sddmdivahovecolofffbackgoud-colo/*ewmeued*/""",
                """</div></BODY></HTML>if(docText.legth>1)vam=$()m.(1%)if(m.()>3)m.css(text-alig,)elseif((.legth==14||.legth==13)&&(.subst(8,2)==24||.subst(8,2)==25||.subst(8,2)==26||.subst(8,2)==27))$().html('')elsevafp=ewFlexPapeViewe('/','',cofigSwfFileescape(swfpath),Scale.6,ZoomTasitio'easeOut',ZoomTime.5,ZoomIteval.2,FitPageOLoadfalse,FitWidthOLoadtue,FullSceeAsMaxWidowfalse,PogessiveLoadigfalse,MiZoomSize.2,MaxZoomSize5,SeachMatchAllfalse,IitViewMode'Potait',PitPapeAsBitmapfalse,ViewModeToolsVisibletue,ZoomToolsVisibletue,NavToolsVisibletue,CusoToolsVisibletue,SeachToolsVisibletue,localeChai'')fuctiohtml_decode(st)vas=if(st.legth==)etus=st.eplace(/&/g,&)//2s=s.eplace(/</g,)s=s.eplace(//g,)s=s.eplace(/'/g,')s=s.eplace(/"/g,)s=s.eplace(//g,)etus.footebode-3pxsolid2C529D.footetdlie-2colo666666paddig-.footetdacolo666666magipxpxtext-.footetdahovecoloFF66网站首页新闻中心法院介绍审务公开法院文化理论研究法官学院司法文书地方法规Copyights©212-216AllRightsReseved.十堰市张湾区人民法院版权所有如有转载或引用本站文章涉及版权问题，请与我们联系地址请添加法院地址邮编请添加法院邮编鄂ICP备121191号-1if(.()).().hef=mailto请添加院长邮箱if(.(jb_mail)).(jb_mail).hef=mailto请添加举报邮箱""",
                """fot-sizefot-familyaddCommettdmagi-ighttext-alig.commetmagi-text-aligbode-bottom1pxdottedgaypaddig-bottom.commetspamagi-ightfot-sizefot-family.comcotetbackgoudgayfot-familypaddig3pxpx3px.233px993pxbackgoudul(/Cotet///zwqfy1)o-epeatmagipxauto.meubgbackgoud-(//Theme5//meu.pg)backgoud-epeatepeat-x/*ewmeu*/sddmmagipaddigz-idex11sddmlimagipaddigoebackgoud--epeatbackgoud-positioightcetelie-9positioelativez-idex11sddmlihovefot-weightboldsddmli.sddmacoloffffot-sizetext-aligcetetext-decoatiooez-idex11bode-ight-stylesolidbode-ight-coloFFFbode-ight-thi9sddmli.sddmahovecoloFFFfot-weightboldsddmli.sddma1coloffffot-sizetext-aligcetetext-decoatiooez-idex111pxsddmli.sddma1hovecoloFFFfot-weightboldsddmdivpositiohidde3pxbackgoud-(//Theme5//tc_bg.pg)bode-bottom4pxsolidmagi14pxpaddigpxpxz-idex11sddmdivapositioelativeowaplie-3pxfot-weightomaltext-decoatiooecolofot-sizepaddig-sddmdivahovecolofffbackgoud-colo/*ewmeued*/""",
                """.htmvaswfpath=//++.swfvaIsCovetSwf=TuevadocText=<!DOCTYPEHTMLPUBLIC-//W3C//DTDHTML4.Tasitioal//EN'><HTML><HEAD><TITLE></TITLE></HEAD><BODY><divstyle='TEXT-ALIGNcete.5ptcm黑体18pt'>湖北省十堰市张湾区人民法院</div><divstyle='TEXT-ALIGNcete.5ptcm黑体18pt'>民事判决书</div><divstyle='TEXT-ALIGNight.5ptcm'>""",
                """</div></BODY></HTML>if(docText.legth>1)vam=$()m.(1%)if(m.()>3)m.css(text-alig,)elseif((.legth==14||.legth==13)&&(.subst(8,2)==24||.subst(8,2)==25||.subst(8,2)==26||.subst(8,2)==27))$().html('')elsevafp=ewFlexPapeViewe('/','',cofigSwfFileescape(swfpath),Scale.6,ZoomTasitio'easeOut',ZoomTime.5,ZoomIteval.2,FitPageOLoadfalse,FitWidthOLoadtue,FullSceeAsMaxWidowfalse,PogessiveLoadigfalse,MiZoomSize.2,MaxZoomSize5,SeachMatchAllfalse,IitViewMode'Potait',PitPapeAsBitmapfalse,ViewModeToolsVisibletue,ZoomToolsVisibletue,NavToolsVisibletue,CusoToolsVisibletue,SeachToolsVisibletue,localeChai'')fuctiohtml_decode(st)vas=if(st.legth==)etus=st.eplace(/&/g,&)//2s=s.eplace(/</g,)s=s.eplace(//g,)s=s.eplace(/'/g,')s=s.eplace(/"/g,)s=s.eplace(//g,)etus.footebode-3pxsolid2C529D.footetdlie-2colo666666paddig-.footetdacolo666666magipxpxtext-.footetdahovecoloFF66网站首页新闻中心法院介绍审务公开法院文化理论研究法官学院司法文书地方法规Copyights©212-216AllRightsReseved.十堰市张湾区人民法院版权所有如有转载或引用本站文章涉及版权问题，请与我们联系地址请添加法院地址邮编请添加法院邮编鄂ICP备121191号-1if(.()).().hef=mailto请添加院长邮箱if(.(jb_mail)).(jb_mail).hef=mailto请添加举报邮箱""",
                """fot-sizefot-familyaddCommettdmagi-ighttext-alig.commetmagi-text-aligbode-bottom1pxdottedgaypaddig-bottom.commetspamagi-ightfot-sizefot-family.comcotetbackgoudgayfot-familypaddig3pxpx3px._ba1218backgoudul(/Cotet///zxsfy1)o-epeatmagipxautosddmlimagipaddigoelie-1positioelativez-idex11sddmdivpositiohiddebackgoud-imageul(//Theme9//tc_bg.pg)bode-bottom4pxsolidmagi14pxpaddigpxpxz-idex11sddmdivapositioelativeowaplie-3pxfot-weightomaltext-decoatiooecolofot-sizepaddig-sddmdivahovecolofffbackgoud-colosddmli.sddmahovecolo333backgoudul(//Theme9//mue_1)epeat-xbottom.meubgxlqfyw124pxlie-2backgoudul(//Theme9//mue2)epeat-xcetemagipxauto""",
                """</div></BODY></HTML>if(docText.legth>1)vam=$()m.(1%)if(m.()>3)m.css(text-alig,)elseif((.legth==14||.legth==13)&&(.subst(8,2)==24||.subst(8,2)==25||.subst(8,2)==26||.subst(8,2)==27))$().html('')elsevafp=ewFlexPapeViewe('/','',cofigSwfFileescape(swfpath),Scale.6,ZoomTasitio'easeOut',ZoomTime.5,ZoomIteval.2,FitPageOLoadfalse,FitWidthOLoadtue,FullSceeAsMaxWidowfalse,PogessiveLoadigfalse,MiZoomSize.2,MaxZoomSize5,SeachMatchAllfalse,IitViewMode'Potait',PitPapeAsBitmapfalse,ViewModeToolsVisibletue,ZoomToolsVisibletue,NavToolsVisibletue,CusoToolsVisibletue,SeachToolsVisibletue,localeChai'')fuctiohtml_decode(st)vas=if(st.legth==)etus=st.eplace(/&/g,&)//2s=s.eplace(/</g,)s=s.eplace(//g,)s=s.eplace(/'/g,')s=s.eplace(/"/g,)s=s.eplace(//g,)etus.mag124pxautomagipxauto.foot1lie-39pxtext-aligcetecolofffbackgoudul(//Theme9//dow)epeat-x.wthacoloffftext-decoatiooe.wthalikcoloffftext-decoatiooe联系我们|设为首页|加入收藏Copyights©212-216AllRightsReseved.湖北省钟祥市人民法院版权所有如有转载或引用本站文章涉及版权问题，请与我们联系地址湖北省荆门市钟祥市王府大道6号邮编4319鄂ICP备121191号-1if(.()).().hef=mailtoif(.(jb_mail)).(jb_mail).hef=mailto""",
                """网站首页新闻中心··法院要闻法院介绍·法院简介·现任院长·机构设置·法院领导湖北法院审务公开·法院公告·工作简报··诉讼须知法院文化··理论研究法律法规·常用法律法规······赔偿文书网站首页""",
                """一、本库公布的由相关法院录入和审核，并依据法律与审判公开的原则予以公开。若有关当事人对相关信息内容有异议的，可向公布法院书面申请更正或者下镜。二、本库提供的信息仅供查询人参考，内容以正式文本为准。非法使用库信息给他人造成损害的，由非法使用人承担法律责任。三、本库信息查询免费，严禁任何单位和个人利用本库信息牟取非法利益。四、未经许可，任何商业性网站不得建立与库及其内容的链接，不得建立本库的镜像（包括全部和局部镜像），不得拷贝或传播本库信息。""",
                """网站首页新闻中心····案件快报法院介绍··现任院长·审务公开·法院公告·司法解释与案例··法院文化··法官摄影·法官书画理论研究·法官讲坛·审判研讨·读书之窗·刑事审判·民商审判·行政审判法官学院······赔偿文书地方法规·法律法规网站首页刘振林与蹇宗宾合伙协议纠纷一审民事判决书公告一、本库公布的由相关法院录入和审核，并依据法律与审判公开的原则予以公开。若有关当事人对相关信息内容有异议的，可向公布法院书面申请更正或者下镜。二、本库提供的信息仅供查询人参考，内容以正式文本为准。非法使用库信息给他人造成损害的，由非法使用人承担法律责任。三、本库信息查询免费，严禁任何单位和个人利用本库信息牟取非法利益。四、未经许可，任何商业性网站不得建立与库及其内容的链接，不得建立本库的镜像（包括全部和局部镜像），不得拷贝或传播本库信息。""",
                """····案件快报法院介绍··现任院长·审务公开·法院公告·司法解释与案例··法院文化··法官摄影·法官书画理论研究·法官讲坛·审判研讨·读书之窗·刑事审判·民商审判·行政审判法官学院······赔偿文书地方法规·法律法规网站首页""",
                """网站首页新闻中心""", """黑体""",
                """fot-sizefot-familyaddCommettdmagi-ighttext-alig.commetmagi-text-aligbode-bottom1pxdottedgaypaddig-bottom.commetspamagi-ightfot-sizefot-family.comcotetbackgoudgayfot-familypaddig3pxpx3pxTabmagipxpaddigpxbode1pxsolidCBCFCE682pxTab.Meuboxfive682px32pxbackgoud-(/Cotet/mastes/ed1_2//tab_title_bg)backgoud-epeatepeat-xTab.MeuboxfiveulmagipxpaddigpxTab.Meuboxfivelicusopoite32pxpaddig-6pxcolo53ABfot-size9pxtext-aligcetebackgoud-(/Cotet/mastes/ed1_2//tab_title_bode)backgoud--epeatbackgoud-positioightTab.Meuboxfiveli.hovebackgoud-(/Cotet/mastes/ed1_2//tab_hove_bg)backgoud-positiocetebackgoud--epeatfot-sizefot-weightbold32pxcoloFFFFFFTab.CotetboxfivecleabothTabuloe.heade228px13pxbackgoud-(/Cotet///gaxfy_h)backgoud--epeatsddmlimagipaddigoebackgoud-imageul(//Theme7//meu_ight_b)backgoud-epeato-epeatbackgoud-positioightcetelie-3px19pxpositioelativez-idex11sddmdivpositiohidde33pxbackgoud-imageul(//Theme7//tc_bg.pg)bode-bottom4pxsolidD532magi14pxpaddigpxpxz-idex11sddmdivapositioelativeowaplie-3pxfot-weightomaltext-decoatiooecolo99fot-sizepaddig-sddmdivahovecolofffbackgoud-coloD532··工作动态·视频新闻法院介绍··现任院长·法院领导审务公开·法院公告··诉讼须知·诉讼问答法院文化·理论研究··法官随笔·法院文化······赔偿文书网站导航网站首页""",
                """</div></BODY></HTML>if(docText.legth>1)vam=$()m.(1%)if(m.()>3)m.css(text-alig,)elseif((.legth==14||.legth==13)&&(.subst(8,2)==24||.subst(8,2)==25||.subst(8,2)==26||.subst(8,2)==27))$().html('')elsevafp=ewFlexPapeViewe('/','',cofigSwfFileescape(swfpath),Scale.6,ZoomTasitio'easeOut',ZoomTime.5,ZoomIteval.2,FitPageOLoadfalse,FitWidthOLoadtue,FullSceeAsMaxWidowfalse,PogessiveLoadigfalse,MiZoomSize.2,MaxZoomSize5,SeachMatchAllfalse,IitViewMode'Potait',PitPapeAsBitmapfalse,ViewModeToolsVisibletue,ZoomToolsVisibletue,NavToolsVisibletue,CusoToolsVisibletue,SeachToolsVisibletue,localeChai'')fuctiohtml_decode(st)vas=if(st.legth==)etus=st.eplace(/&/g,&)//2s=s.eplace(/</g,)s=s.eplace(//g,)s=s.eplace(/'/g,')s=s.eplace(/"/g,)s=s.eplace(//g,)etus.avfot-sizelie-33pxcolo666backgoud-coloe8e6e6text-aligcete33px1pxmagipxauto.black_wzacolo333fotatext-aliktext-网站首页|新闻中心|法院介绍|法院文化||司法文书Copyights©212-216AllRightsReseved.公安县人民法院版权所有如有转载或引用本站文章涉及版权问题，请与我们联系地址荆州市公安县斗湖堤镇治安路2号邮编4343鄂ICP备121191号-1if(.()).().hef=mailtoif(.(jb_mail)).(jb_mail).hef=mailto""",
                '法院领导', '机构设置湖北法院审务公开', '法院公告', '案例指导', '机构名称', '楚天审判', '诉讼须知',
                '诉讼问答法院文化', '法官摄影理论研究', '法官论坛法官学院', '赔偿文书网站导航网站首页', '执行文书网站导航网站首页', '民事文书网站导航网站首页', '行政文书网站导航网站首页',
                '法庭在线视频', '新闻法院', '新闻法院', '介绍机构', '设置审务', '公开精品案例', '审判动态', '律师投诉', '人民陪审', '机构名册', '失信被执行人', '律师权利保障',
                '法官博客',
                '文化阵地', '理论研究', '法官论坛', '网友争鸣', '调查研究', '读书园地', '院长推荐', '精品赏析', '民事刑事行政赔偿文书', '党建工作', '组织队伍', '制度活动',
                '廉政建设网站首页', '网站首页', '新闻中心', '法院介绍', '机构设置', '精品案例', '诉讼问答', '法院文化', '廉政建设',
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                'V',  ' ', '\t', '\n', '\r',
                'W', 'X', 'Y', 'Z',
                '-', '.', '(', ')', '/', '·', '本院介绍', '现任院长', "''", "|", "&", "$", "_", "@", "#", '<', ">", '=', "'", "%", ",,",
                '13030016826823212003260053901212321240199336000000**0000339114000000099000053200**', '130310218009400000009033309120920',
                '1303005903223103**0000982440072304100000723', '130311891003011281000033990000702440499000049049244049900040',
                '1303001682682321200326005390121232100331', '{{{，{{{1682{6823212{{32600539012{1232{{{12401{9933600000**{{33{{{1{1{',
                '519685329774583145963471288++200,Ã©ÂÂÃ¥ÂÂÃ§ÂÂ´Ã¦ÂÂ¥Ã¨Â¿ÂÃ¥ÂÂÃÂ!,Ã¨Â¶ÂÃ¨Â¿ÂÃ¦ÂÂÃ¦ÂÂ¬Ã©ÂÂ¿Ã¥ÂºÂ¦Ã§ÂÂ´Ã¦ÂÂ¥Ã¨Â¿ÂÃ¥ÂÂÃÂ提示关闭电子送达协议同意拒绝51关闭，我是小宇~欢迎使用，有问题可点击问我！0消息（0）0待办（0）咨询小宇风险评估在线诉状类案查询法律法规电子诉讼智能助手问答待办3消息2工具发送全部清空3750查看详情页面+?+++返回登录注册甘肃法院诉讼无忧3750增加样式判断750首页详情公开是依据国家有关法律及最高人民法院等相关规定，相关事宜请与宣判法院联系',]

        for i in range(3):
            for w in data:
                s = s.replace(w, '')
        for w in data:
            s = s.replace(w, '')
        return s

    def deal_caseType(self, caseType, wstype):
        if '民事' in caseType:
            return '民事'+wstype
        if '行政' in caseType:
            return '行政'+wstype
        if '执行' in caseType:
            return '执行'+wstype
        if '刑事' in caseType:
            return '刑事'+wstype
        if '赔偿' in caseType:
            return '赔偿'+wstype
        else:
            return caseType

    def start_requests(self):
        last_id = self.select_data(['minid'], 'adjudicative', 'xd_updateid', cond="""where `table` = 'caipan_closed'""")[0][0]
        all_id = self.select_data(['id'], 'adjudicative', 'caipan_closed', cond="""where id > '{last_id}'""".format(last_id=last_id))
        # all_id = self.select_data(['id'], 'adjudicative', 'caipan_closed', cond='order by id limit 100')
        self.update_data(['minid'], [max(all_id)[0]], 'adjudicative', 'xd_updateid', where="""`table`='{table}'""".format(table='caipan_closed'))
        for i in all_id:
            caipan_id = i[0]
            self.send_mqdata(caipan_id)

    def parse_only(self, body):
        caipan_id = body
        caipan_data = self.select_data(['id', 'title', 'wslx', 'caseNo', 'sortTime', 'posttime', 'court', 'caseType',
                                        'body', 'detailUrl', 'province', 'MD5', 'source'],
                                       'adjudicative', 'caipan_closed', where="""id={id}""".format(id=caipan_id))[0]
        id = caipan_data[0]
        title = caipan_data[1]
        wslx = caipan_data[2]
        caseNo = caipan_data[3]
        sortTime = caipan_data[4]
        posttime = caipan_data[5]
        court = caipan_data[6]
        caseType = caipan_data[7]
        body = caipan_data[8]
        detailUrl = caipan_data[9]
        province = caipan_data[10]
        source = caipan_data[11]


        posttime = self.parseDate(posttime)
        sortTime = self.parseDate(sortTime)
        item = {}
        item['wid'] = id
        item['title'] = title
        item['province'] = province
        item['court'] = court
        item['CASENO'] = caseNo
        item['sdate'] = sortTime
        item['pdate'] = posttime
        item['caseType'] = self.deal_caseType(caseType, wslx)
        item['url'] = detailUrl
        item['source'] = source
        # self.insert(item, 'rizhi_court_cpws')
        self.prints(item)

        content_item = {}
        s = Selector(text=body.replace('\\"', '"').replace('\\\\', ''))
        body_demo = self.data_deal(''.join(s.xpath('//text()').extract()))
        content_item['wid'] = caipan_id
        content_item['content'] = body_demo
        # self.insert(content_item, 'rizhi_court_cpws_content')
        self.prints(content_item)


if __name__ == '__main__':
    start_run = update_caipan_close()
    start_run.run('update_caipan_close')