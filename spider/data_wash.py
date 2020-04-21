# -*- coding: utf-8 -*-
from config.all_config import *

class data_wash(Manager):
    name = 'data_wash'

    def __init__(self):
        Manager.__init__(self, 'ysh_data_wash')
        self.content = re.compile('prepend\(unescape\("(.*?)"\)\);', re.S)
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

    def wash_date(self, content):
        rep = [
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
            """网站首页新闻中心""",
            """fot-sizefot-familyaddCommettdmagi-ighttext-alig.commetmagi-text-aligbode-bottom1pxdottedgaypaddig-bottom.commetspamagi-ightfot-sizefot-family.comcotetbackgoudgayfot-familypaddig3pxpx3pxTabmagipxpaddigpxbode1pxsolidCBCFCE682pxTab.Meuboxfive682px32pxbackgoud-(/Cotet/mastes/ed1_2//tab_title_bg)backgoud-epeatepeat-xTab.MeuboxfiveulmagipxpaddigpxTab.Meuboxfivelicusopoite32pxpaddig-6pxcolo53ABfot-size9pxtext-aligcetebackgoud-(/Cotet/mastes/ed1_2//tab_title_bode)backgoud--epeatbackgoud-positioightTab.Meuboxfiveli.hovebackgoud-(/Cotet/mastes/ed1_2//tab_hove_bg)backgoud-positiocetebackgoud--epeatfot-sizefot-weightbold32pxcoloFFFFFFTab.CotetboxfivecleabothTabuloe.heade228px13pxbackgoud-(/Cotet///gaxfy_h)backgoud--epeatsddmlimagipaddigoebackgoud-imageul(//Theme7//meu_ight_b)backgoud-epeato-epeatbackgoud-positioightcetelie-3px19pxpositioelativez-idex11sddmdivpositiohidde33pxbackgoud-imageul(//Theme7//tc_bg.pg)bode-bottom4pxsolidD532magi14pxpaddigpxpxz-idex11sddmdivapositioelativeowaplie-3pxfot-weightomaltext-decoatiooecolo99fot-sizepaddig-sddmdivahovecolofffbackgoud-coloD532··工作动态·视频新闻法院介绍··现任院长·法院领导审务公开·法院公告··诉讼须知·诉讼问答法院文化·理论研究··法官随笔·法院文化······赔偿文书网站导航网站首页""",
            """</div></BODY></HTML>if(docText.legth>1)vam=$()m.(1%)if(m.()>3)m.css(text-alig,)elseif((.legth==14||.legth==13)&&(.subst(8,2)==24||.subst(8,2)==25||.subst(8,2)==26||.subst(8,2)==27))$().html('')elsevafp=ewFlexPapeViewe('/','',cofigSwfFileescape(swfpath),Scale.6,ZoomTasitio'easeOut',ZoomTime.5,ZoomIteval.2,FitPageOLoadfalse,FitWidthOLoadtue,FullSceeAsMaxWidowfalse,PogessiveLoadigfalse,MiZoomSize.2,MaxZoomSize5,SeachMatchAllfalse,IitViewMode'Potait',PitPapeAsBitmapfalse,ViewModeToolsVisibletue,ZoomToolsVisibletue,NavToolsVisibletue,CusoToolsVisibletue,SeachToolsVisibletue,localeChai'')fuctiohtml_decode(st)vas=if(st.legth==)etus=st.eplace(/&/g,&)//2s=s.eplace(/</g,)s=s.eplace(//g,)s=s.eplace(/'/g,')s=s.eplace(/"/g,)s=s.eplace(//g,)etus.avfot-sizelie-33pxcolo666backgoud-coloe8e6e6text-aligcete33px1pxmagipxauto.black_wzacolo333fotatext-aliktext-网站首页|新闻中心|法院介绍|法院文化||司法文书Copyights©212-216AllRightsReseved.公安县人民法院版权所有如有转载或引用本站文章涉及版权问题，请与我们联系地址荆州市公安县斗湖堤镇治安路2号邮编4343鄂ICP备121191号-1if(.()).().hef=mailtoif(.(jb_mail)).(jb_mail).hef=mailto""",
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z',
            'A' 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
            'W', 'X', 'Y', 'Z',
            '-', '.', '(', ')', '/', '·', '本院介绍', '现任院长', "''", "|", "&", "$", "_",
            '法院领导', '机构设置湖北法院审务公开', '法院公告', '案例指导', '机构名称', '楚天审判', '诉讼须知', '<', ">", '=', "'", "%", ",,",
            '诉讼问答法院文化', '法官摄影理论研究', '法官论坛法官学院', '赔偿文书网站导航网站首页', '执行文书网站导航网站首页', '民事文书网站导航网站首页', '行政文书网站导航网站首页',
            '法庭在线视频', '新闻法院', '新闻法院', '介绍机构', '设置审务', '公开精品案例', '审判动态', '律师投诉', '人民陪审', '机构名册', '失信被执行人', '律师权利保障', '法官博客',
            '文化阵地', '理论研究', '法官论坛', '网友争鸣', '调查研究', '读书园地', '院长推荐', '精品赏析', '民事刑事行政赔偿文书', '党建工作', '组织队伍', '制度活动', '廉政建设网站首页'
            ]
        for a in range(2):
            for i in rep:
                content = content.replace(i, '')
        return content

    def start_requests(self):
        all_none = self.select_data(['wid'], 'el_rizhi', 'rizhi_court_cpws_content', where="""content=''""")
        for i in all_none:
            wid = i[0]
            content_url = self.select_data(['url'], 'el_rizhi', 'rizhi_court_cpws', where="""wid={wid}""".format(wid=wid))[0][0]
            self.send_mqdata(content_url+'~'+str(wid))

    def parse_only(self, body):
        url = body.split('~')[0]
        wid = body.split('~')[1]
        request = MyRequests(url=url, headers=self.header, callback='get_content', meta={'wid': wid}, timeout=15)
        self.send_mqdata(request)

    def get_content(self, response):
        if '不公开理由' in response.text:
            s = Selector(text=response.text)
            content = self.data_deal(''.join(s.xpath('//table[@id="cc"]/div/text()').extract()))
            print('修改后：', self.now_time(), content)
            self.update_data(field_lists=['content'], values_lists=[content], db_name='el_rizhi', table='rizhi_court_cpws_content', where='wid={wid}'.format(wid=response.meta['wid']))
        else:
            try:
                content = self.data_deal(self.deal_re(self.content.search(response)).encode('latin-1').decode('unicode_escape'))
                if content:
                    s = Selector(text=content)
                    content = self.data_deal(''.join(s.xpath('//text()').extract()))
                    print('修改后：', self.now_time(), content)
                    self.update_data(field_lists=['content'], values_lists=[content], db_name='el_rizhi', table='rizhi_court_cpws_content', where='wid={wid}'.format(wid=response.meta['wid']))
            except:
                s = Selector(text=response.text)
                content = self.data_deal(''.join(s.xpath('//text()').extract()))
                print('修改后：', self.now_time(), content)
                self.update_data(field_lists=['content'], values_lists=[content], db_name='el_rizhi', table='rizhi_court_cpws_content', where='wid={wid}'.format(wid=response.meta['wid']))
        print('=================================================')
        return

if __name__ == '__main__':
    start_run = data_wash()
    start_run.run('data_wash')