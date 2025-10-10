BEGIN;

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1360, '2025-09-10 15:22:45', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1080, '2025-09-10 10:16:55', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1090, '2025-09-10 12:04:38', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1480, '2025-09-10 17:18:08', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ハムサンド', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1130, '2025-09-10 11:25:30', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1120, '2025-09-11 14:04:30', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 630, '2025-09-11 15:26:10', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1210, '2025-09-11 13:39:56', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 660, '2025-09-11 17:39:31', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 870, '2025-09-11 15:59:29', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 350, '2025-09-11 18:34:20', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 430, '2025-09-12 13:46:58', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 410, '2025-09-12 14:58:40', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 510, '2025-09-12 10:37:29', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 690, '2025-09-12 09:09:26', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 530, '2025-09-12 17:45:18', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1190, '2025-09-12 12:51:38', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ハムサンド', 320);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1150, '2025-09-12 14:44:08', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ハムサンド', 320);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 790, '2025-09-13 18:26:35', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 860, '2025-09-13 17:06:27', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 830, '2025-09-13 09:01:28', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 820, '2025-09-13 14:11:01', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ハムサンド', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 830, '2025-09-13 17:16:37', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 560, '2025-09-13 17:19:30', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1160, '2025-09-13 15:15:42', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 720, '2025-09-14 14:25:05', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1020, '2025-09-14 17:49:13', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 740, '2025-09-14 09:45:45', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 740, '2025-09-14 11:20:18', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1300, '2025-09-14 13:04:29', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1050, '2025-09-14 14:15:21', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 930, '2025-09-14 12:19:53', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1150, '2025-09-15 17:06:17', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 450, '2025-09-15 12:04:38', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 850, '2025-09-15 10:21:55', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1330, '2025-09-15 10:08:03', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1230, '2025-09-15 14:02:04', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 490, '2025-09-16 17:23:34', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1390, '2025-09-16 15:46:11', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 840, '2025-09-16 16:43:31', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1150, '2025-09-16 18:12:53', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1430, '2025-09-16 18:38:54', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1170, '2025-09-16 19:55:34', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 710, '2025-09-17 12:56:51', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1360, '2025-09-17 19:27:29', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 750, '2025-09-17 10:25:44', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 700, '2025-09-17 15:55:03', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ハムサンド', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1050, '2025-09-17 14:41:50', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 640, '2025-09-18 09:35:27', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ハムサンド', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1030, '2025-09-18 10:19:24', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 870, '2025-09-18 16:29:56', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1320, '2025-09-18 17:53:30', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1110, '2025-09-18 11:46:54', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 770, '2025-09-19 11:30:23', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1400, '2025-09-19 17:06:22', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1400, '2025-09-19 17:50:34', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ハムサンド', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 380, '2025-09-19 13:57:00', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 820, '2025-09-19 18:27:58', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 980, '2025-09-19 14:11:27', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1350, '2025-09-20 11:42:18', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 680, '2025-09-20 11:08:16', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 840, '2025-09-20 11:16:26', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1260, '2025-09-20 10:03:28', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 500, '2025-09-20 12:41:25', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 430, '2025-09-20 12:17:40', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1320, '2025-09-20 19:19:07', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 860, '2025-09-21 13:15:12', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ハムサンド', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1110, '2025-09-21 14:25:53', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 540, '2025-09-21 11:52:34', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 790, '2025-09-21 12:46:30', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 840, '2025-09-21 18:48:59', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1310, '2025-09-21 17:49:44', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1610, '2025-09-22 15:16:15', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 790, '2025-09-22 14:48:27', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 480, '2025-09-22 12:56:19', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 420, '2025-09-22 12:59:26', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 380, '2025-09-22 17:51:06', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 930, '2025-09-22 17:54:02', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 700, '2025-09-22 12:42:07', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 600, '2025-09-22 12:14:48', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 940, '2025-09-23 14:33:04', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 610, '2025-09-23 16:34:48', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 990, '2025-09-23 09:11:12', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 550, '2025-09-23 17:02:08', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1140, '2025-09-23 12:03:13', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1330, '2025-09-23 17:08:58', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 670, '2025-09-24 13:38:37', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1320, '2025-09-24 11:38:33', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ハムサンド', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1510, '2025-09-24 09:44:30', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1330, '2025-09-24 11:09:45', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 320, '2025-09-24 10:30:39', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 500, '2025-09-24 15:18:36', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 460, '2025-09-25 18:47:01', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1170, '2025-09-25 10:12:18', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ハムサンド', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 690, '2025-09-25 16:37:41', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 740, '2025-09-25 19:11:04', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 810, '2025-09-25 10:37:25', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ハムサンド', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1220, '2025-09-26 18:16:24', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ハムサンド', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 760, '2025-09-26 17:58:58', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 540, '2025-09-26 11:48:51', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 670, '2025-09-26 11:09:19', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 820, '2025-09-26 13:15:18', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1340, '2025-09-27 19:03:45', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 400, '2025-09-27 19:41:28', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 890, '2025-09-27 13:30:10', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 950, '2025-09-27 10:42:49', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 700, '2025-09-27 17:16:39', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 900, '2025-09-27 11:46:35', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 440, '2025-09-27 13:31:11', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 870, '2025-09-27 13:27:44', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 880, '2025-09-28 16:25:27', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1020, '2025-09-28 15:19:34', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 700, '2025-09-28 16:10:02', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1130, '2025-09-28 11:03:47', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1420, '2025-09-28 19:17:10', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 960, '2025-09-28 14:23:16', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1310, '2025-09-29 14:53:18', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 510, '2025-09-29 17:15:32', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 970, '2025-09-29 18:05:05', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1100, '2025-09-29 13:28:42', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 980, '2025-09-29 11:32:04', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1310, '2025-09-30 11:04:29', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 850, '2025-09-30 11:16:20', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1270, '2025-09-30 12:51:55', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 330, '2025-09-30 15:54:00', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1030, '2025-09-30 13:31:24', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1470, '2025-10-01 11:15:30', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 820, '2025-10-01 19:28:03', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 630, '2025-10-01 17:50:39', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1240, '2025-10-01 17:22:38', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 410, '2025-10-01 18:31:06', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 560, '2025-10-01 19:46:47', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1110, '2025-10-01 12:16:16', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 830, '2025-10-01 15:50:21', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1000, '2025-10-02 13:22:30', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 980, '2025-10-02 15:14:45', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 510, '2025-10-02 14:11:45', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 990, '2025-10-02 16:25:40', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 770, '2025-10-02 11:29:04', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ハムサンド', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 820, '2025-10-02 18:48:34', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1100, '2025-10-02 18:08:58', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1290, '2025-10-02 14:28:03', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 410, '2025-10-03 13:14:47', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 870, '2025-10-03 09:41:56', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1270, '2025-10-03 19:29:54', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 890, '2025-10-03 19:08:06', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1380, '2025-10-03 12:59:53', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ハムサンド', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 780, '2025-10-03 18:43:05', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 570, '2025-10-03 17:31:39', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1190, '2025-10-03 12:33:23', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 500, '2025-10-04 12:18:43', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 850, '2025-10-04 18:48:10', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 660, '2025-10-04 18:36:17', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1000, '2025-10-04 16:30:42', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1040, '2025-10-04 18:51:10', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 710, '2025-10-04 13:56:53', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1140, '2025-10-04 17:02:05', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1180, '2025-10-04 09:04:24', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 610, '2025-10-05 11:59:44', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 960, '2025-10-05 14:54:16', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 400, '2025-10-05 18:14:53', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 350, '2025-10-05 09:14:05', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 530, '2025-10-05 15:08:27', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 490, '2025-10-05 12:16:01', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1390, '2025-10-05 15:20:41', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 410, '2025-10-05 13:33:03', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1090, '2025-10-06 17:54:19', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1090, '2025-10-06 19:02:14', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 880, '2025-10-06 13:28:52', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1320, '2025-10-06 11:52:27', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1140, '2025-10-06 16:44:33', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1290, '2025-10-06 15:50:53', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1070, '2025-10-06 16:59:11', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1370, '2025-10-06 17:35:41', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 990, '2025-10-07 14:28:36', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 390, '2025-10-07 19:18:16', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 500, '2025-10-07 19:53:31', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 300, '2025-10-07 16:02:18', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1150, '2025-10-07 11:15:36', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 500, '2025-10-08 14:36:45', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1560, '2025-10-08 15:21:51', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ハムサンド', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 850, '2025-10-08 11:07:36', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 990, '2025-10-08 14:52:49', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 950, '2025-10-08 16:17:14', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 880, '2025-10-08 10:43:18', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1240, '2025-10-08 17:09:38', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '塩パン', 160);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 1070, '2025-10-09 14:24:11', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1210, '2025-10-09 13:03:22', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ベーグル', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ハムサンド', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1510, '2025-10-09 13:42:06', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ハムサンド', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 1210, '2025-10-09 19:35:36', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 970, '2025-10-09 17:55:16', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナサンド', 290);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームコロネ', 190);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 720, '2025-10-09 13:46:46', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'バゲット', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 350, '2025-10-09 11:27:37', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クロワッサン', 200);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 430, '2025-10-09 09:37:17', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 620, '2025-10-10 14:04:13', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 640, '2025-10-10 13:34:41', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '焼きそばパン', 230);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'シナモンロール', 240);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1280, '2025-10-10 12:06:27', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'デニッシュ', 210);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 570, '2025-10-10 14:26:49', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ハムサンド', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコクロワッサン', 250);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 760, '2025-10-10 12:45:14', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'クリームパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1010, '2025-10-10 17:59:52', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 750, '2025-10-10 09:48:19', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 330, '2025-10-10 09:07:54', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'メロンパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'あんぱん', 150);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 880, '2025-10-11 17:39:39', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チーズパン', 180);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'コロッケパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'くるみパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'よもぎあんぱん', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 820, '2025-10-11 16:33:04', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ハムサンド', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 1130, '2025-10-11 17:04:18', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ロールパン', 140);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'たまごサンド', 280);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ツナマヨパン', 200);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ピザパン', 250);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'アップルパイ', 260);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (1, 3, 'パン工房', 790, '2025-10-11 12:57:51', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'チョコパン', 170);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (3, 3, 'パン工房', 830, '2025-10-11 13:56:37', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ハムサンド', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'ソーセージパン', 190);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipts (user_id, store_id, supplier_name, total_amount, receipt_date, created_at, updated_at)
VALUES (2, 3, 'パン工房', 840, '2025-10-11 13:50:43', NOW(), NOW());

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'フランスパン', 320);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), '食パン', 300);

INSERT INTO receipt_items (receipt_id, description, amount)
VALUES (currval('receipts_id_seq'), 'カレーパン', 220);

COMMIT;

-- 挿入されたデータの確認
SELECT COUNT(*) as total_receipts FROM receipts WHERE store_id = 3 AND receipt_date >= '2025-09-10' AND receipt_date <= '2025-10-11';
SELECT MIN(receipt_date) as earliest, MAX(receipt_date) as latest FROM receipts WHERE store_id = 3 AND receipt_date >= '2025-09-10' AND receipt_date <= '2025-10-11';
