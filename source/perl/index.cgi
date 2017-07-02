#!/usr/local/bin/perl --
use DBI;
use CGI;

$q = new CGI;

# 各種定数設定
$page_title    = "第十四回博麗神社例大祭　小説サークルまとめ";
$event_name    = "第十四回博麗神社例大祭";
$author        = "東方天翔記CPUダービー処(鍵山ゆーな)";
$keywords      = "東方, 小説, 例大祭14, rts14";
$page_url      = "http://www.thtenshouki.info/rts14_thnovels/";
$description   = "例大祭14で頒布予定の東方小説についてのまとめ。品質(正確性・網羅性)に過度の期待をしないように。";
$tweet_hashtag = "";
$hearing_url   = "https://goo.gl/forms/bMCKNAKR9WcINcPs1";

# DB接続
$d = "";
$u = "";
$p = "";

$dbh = DBI->connect($d, $u, $p, {'RaiseError' => 1});
$dbh->do("set names utf8");

print << "EOT_HEAD_1";
Content-Type: text/html; charset=UTF-8;

<!DOCTYPE HTML>
<!--
	Hyperspace by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<html>
	<head>
		<title>${page_title}</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<meta name="description" content="${description}" />
		<meta name="keywords" content="${keywords}" />
		<meta name="author" content="${author}" />
		<!--[if lte IE 8]><script src="assets/js/ie/html5shiv.js"></script><![endif]-->
		<link rel="stylesheet" href="assets/css/main.css" />
		<!--[if lte IE 9]><link rel="stylesheet" href="assets/css/ie9.css" /><![endif]-->
		<!--[if lte IE 8]><link rel="stylesheet" href="assets/css/ie8.css" /><![endif]-->
		<!-- Facebook and Twitter integration -->
		<meta property="og:title" content="${page_title}"/>
		<meta property="og:image" content=""/>
		<meta property="og:url" content="${page_url}"/>
		<meta property="og:site_name" content=""/>
		<meta property="og:description" content="${description}"/>
		<meta name="twitter:title" content="${page_title}" />
		<meta name="twitter:image" content="" />
		<meta name="twitter:url" content="${page_url}" />
		<meta name="twitter:card" content="" />
	</head>

	<body>

		<!-- Sidebar -->
			<section id="sidebar">
				<div class="inner">
					<nav>
						<ul>
							<li><a href="#intro">このページについて</a></li>
EOT_HEAD_1

$quoted_str = "select substring(space_no, 1, 1) grp, count(*) cnt from toho_novels where event_name = '$event_name' group by grp;";
$sth = $dbh->prepare($quoted_str);
$sth->execute;

$rowcnt = $sth->rows;
for ($cnt = 0; $cnt < $rowcnt; $cnt++) {
  @rec = $sth->fetchrow_array;
  $space = $rec[0];
  $num = $rec[1];
  print "							<li><a href=\"#${space}\">${space}島 (${num})</a></li>\n";
}

print << "EOT_HEAD_2";
							<li><a href="https://twitter.com/share" class="twitter-share-button" data-url="${page_url}" data-text="${page_title} ${tweet_hashtag}" data-lang="ja">ツイート</a>
<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');</script></li>
							<li><a href="${hearing_url}" target="_blank">利用者アンケート</a></li>
						</ul>
					</nav>
				</div>
			</section>

		<!-- Wrapper -->
			<div id="wrapper">
				<!-- Intro -->
					<section id="intro" class="wrapper style1 fullscreen fade-up">
						<div class="inner">
							<h1>このページについて</h1>
							<p>${event_name}で頒布予定の東方小説についてのまとめ。既刊の情報は当ページ内には掲載しない。<br />以下記法に従って掲載された情報を一日一回程度収集して更新する。<br />
							<div class="12u\$"><span class="image fit"><img src="images/rule.png" alt="" /></span></div><br />
							<br />
							<font color="#FF0000"><b>品質(正確性・網羅性)に過度の期待をしないように。</b></font><br />お問い合わせは<a href="https://twitter.com/yuna_priest" target="_blank">こちら</a>までリプライをください</p>
						</div>
					</section>

EOT_HEAD_2

$island = "";
$quoted_str = "SELECT circle_name, space_no, pen_name, new_books, new_book_values, url, web_catalog_url, twitter, tag, shops FROM `toho_novels` where event_name = '$event_name' order by space_no;";
$sth = $dbh->prepare($quoted_str);
$sth->execute;

$rowcnt = $sth->rows;
for ($cnt = 0; $cnt < $rowcnt; $cnt++) {
  @tmp = $sth->fetchrow_array;
  $nowisland_mark = $tmp[1];
  utf8::decode($nowisland_mark);
  $nowisland = substr($nowisland_mark, 0, 1);
  utf8::encode($nowisland);
  
  if ($island eq "") {
    $island = $nowisland;
    print << "EOT_DIV_HEAD";
				<!-- One -->
					<blockquote><h2>${island}島</h2></blockquote>
					<section id="$island">
EOT_DIV_HEAD
  } elsif ($island ne $nowisland) {
    $island = $nowisland;
    print << "EOT_DIV";
					</section>
					<blockquote><h2>${island}島</h2></blockquote>
					<section id="$island">
EOT_DIV

  }
  
  # Webカタログリンク生成
  $catalog = "<a href='$tmp[6]' target='_blank'>$tmp[1]</a>";
  # サークルHPリンク生成
  $circle = $tmp[0];
  if ($tmp[5] ne "") {
    $circle = "<a href='$tmp[5]' target='_blank'>$tmp[0]</a>";
  }
  # ツイッターリンク生成
  $twitter = "";
  if ($tmp[7] ne "") {
    $twitter = "<a href='$tmp[7]' target='_blank' class='icon fa-twitter'><span class='label'>Twitter</span></a>";
  }
  # タグ
  $tag = "$tmp[8]";
  $tag =~ s|/|</li><li>|g;
  # 新刊情報
  $newbook = "$tmp[3]";
  @newbooklist = split(/\//, $newbook);
  $newbook_val = "$tmp[4]";
  @newbook_vallist = split(/\//, $newbook_val);
  $newbook_mark = "";
  if ($newbook ne "") {
    $newbook_mark = "<small><b style=\"color: #C16543;\">新刊あり</b></small>";
  }
  $r18 = "";
  if (index($tag, "R-18") > -1) {
    $r18 = "<h6><span style=\"color: #ff0000; text-shadow: 1px 1px 0.5px #777777;\">当該サークルの新刊または既刊にはR-18作品が含まれています。<br />青年向け同人誌を18歳未満の方への頒布すること及び試読させることは、<br />「東京都青少年の健全な育成に関する条例」により禁じられております。<br />（これに違反した場合、サークル及び会場たる東京ビッグサイト及び主催者たる博麗神社社務所が処罰の対象となり得ます。）<br />購入時には年齢を確認できる公的な身分証明書（免許証・旅券等）を持参ください。<br />また、列形成時は身分証明書をお手元にご用意してお待ちください。<br />皆様のご理解・ご協力をよろしくお願い致します。</span></h6>";
  }
  
  # 委託
  $itaku = "委託情報なし";
  if ($tmp[9] ne "") {
    $itaku = "<ul class=\"actions\">";
    @itakulist = split(/,/, $tmp[9]);
    for ($i = 0; $i < $#itakulist + 1; $i++) {
      if (index($itakulist[$i], "melonbooks") > -1) {
        $itaku = $itaku . "<li><a href=\"$itakulist[$i]\" target=\"_blank\" class=\"button\">🍈メロンブックス</a></li>";
      } elsif (index($itakulist[$i], "toranoana") > -1) {
        $itaku = $itaku . "<li><a href=\"$itakulist[$i]\" target=\"_blank\" class=\"button\">🐯とらのあな</a></li>";
      } else {
        $itaku = $itaku . "<li><a href=\"$itakulist[$i]\" target=\"_blank\" class=\"button\">🏢その他ショップ・自家通販等</a></li>";
      }
    }
    $itaku = $itaku . "</ul>";
  }
  
  print << "EOT_DESC_1";
						<section class="wrapper style2 spotlights">
							<section>
								<div class="content">
									<span data-position="center center"><h3>$catalog　$circle</h3><h6>$newbook_mark</h6>$r18</span>
									<div class="inner">
										<br />
										サークル代表者(申込者)　：　$tmp[2]　$twitter<br />
										<br />
										<h3>新刊</h3>
										<table class="alt">
											<thead>
												<tr>
													<td>新刊タイトル(判型・ページ数)</td>
													<td>価格</td>
												</tr>
											</thead>
EOT_DESC_1

  for ($i = 0; $i < $#newbooklist + 1; $i++) {
    print "											<tr><td>$newbooklist[$i]</td><td>$newbook_vallist[$i] 円</td></tr>\n";
  }
  if ($i == 0) {
    print "											<tfoot><tr><td colspan=\"2\">（新刊なし）</td></tr></tfoot>\n";
  }
  
  print << "EOT_DESC_2";
										</table>
										<h3>タグ</h3>
										<ul><li>$tag</li></ul>
										<h3>委託</h3>
										$itaku
									</div>
								</div>
							</section>
						</section>
EOT_DESC_2

}

print << "EOT_FOOT";
					</section>
			</div>
		<!-- Footer -->
			<footer id="footer" class="wrapper style1-alt">
				<div class="inner">
					<img src="http://www.thtenshouki.info/site_counter.cgi?site=rts14" border="0" />
					<ul class="menu">
						<li>Powerd by <a href="http://www.thtenshouki.info" target="_blank">東方天翔記CPUダービー処</a></li><li>Design: <a href="http://html5up.net">HTML5 UP</a></li><li>Program & Script: <a href="https://twitter.com/yuna_priest" target="_blank">Yuna Kagiyama</a></li>
					</ul>
				</div>
			</footer>

		<!-- Scripts -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrollex.min.js"></script>
			<script src="assets/js/jquery.scrolly.min.js"></script>
			<script src="assets/js/skel.min.js"></script>
			<script src="assets/js/util.js"></script>
			<!--[if lte IE 8]><script src="assets/js/ie/respond.min.js"></script><![endif]-->
			<script src="assets/js/main.js"></script>

	</body>
</html>
EOT_FOOT

# DB切断
$dbh->disconnect();

