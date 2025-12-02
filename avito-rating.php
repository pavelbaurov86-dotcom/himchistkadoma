<?php
// avito-rating.php
// Простой скрипт, который подтягивает рейтинг и количество отзывов с вашей страницы Авито.
// ВАЖНО: структура страницы Авито может меняться, и тогда селекторы ниже нужно будет обновить.

header('Content-Type: application/json; charset=utf-8');

// URL вашей страницы на Авито
$url = 'https://www.avito.ru/brands/i1033191?gdlkerfdnwq=101&iid=2629033365&item_type=str_trx&page_from=from_item_header&page_from=from_item_card&iid=2629033365';

// Настройки cURL
$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (compatible; HimchistkaDomaBot/1.0)');
curl_setopt($ch, CURLOPT_TIMEOUT, 10);

$html = curl_exec($ch);
$err  = curl_error($ch);
$code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($err || !$html || $code >= 400) {
    echo json_encode([
        'ok' => false,
        'error' => 'curl_error',
        'message' => $err,
        'http_code' => $code,
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

// Парсим HTML
libxml_use_internal_errors(true);
$dom = new DOMDocument();
$dom->loadHTML($html);
libxml_clear_errors();

$xpath = new DOMXPath($dom);

// Рейтинг: элемент с data-marker="profile/score"
$ratingNode = $xpath->query("//*[@data-marker='profile/score']")->item(0);
$rating = $ratingNode ? trim($ratingNode->textContent) : null;

// Кол-во отзывов: элемент с data-marker="profile/summary"
$reviewsNode = $xpath->query("//*[@data-marker='profile/summary']")->item(0);
$reviewsText = $reviewsNode ? trim($reviewsNode->textContent) : null;

// Пытаемся достать голое число из текста "201 отзыв"
$reviewsNumber = null;
if ($reviewsText) {
    if (preg_match('/\d+/', $reviewsText, $m)) {
        $reviewsNumber = $m[0];
    }
}

echo json_encode([
    'ok'           => true,
    'rating'       => $rating,
    'reviews'      => $reviewsNumber,
    'reviews_text' => $reviewsText,
], JSON_UNESCAPED_UNICODE);
