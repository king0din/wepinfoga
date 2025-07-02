#!/usr/bin/env python3
"""
Bilgi Toplama Botu - Entegrasyon Test Scripti
Bu script, sistemin tüm bileşenlerini test eder.
"""

import requests
import json
import time
import sys

# Test ayarları
WEB_SERVER_URL = "http://localhost:5004"
TEST_USER_ID = 123456789

def test_web_server_health():
    """Web sunucusunun çalışıp çalışmadığını test et"""
    print("🔍 Web sunucusu sağlık kontrolü...")
    try:
        response = requests.get(f"{WEB_SERVER_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Web sunucusu çalışıyor")
            return True
        else:
            print(f"❌ Web sunucusu hata döndü: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Web sunucusuna bağlanılamadı: {e}")
        return False

def test_create_link_api():
    """Bağlantı oluşturma API'sini test et"""
    print("\n🔍 Bağlantı oluşturma API testi...")
    try:
        data = {"sender_telegram_id": TEST_USER_ID}
        response = requests.post(
            f"{WEB_SERVER_URL}/api/create_link",
            json=data,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            tracking_id = result.get('tracking_id')
            tracking_url = result.get('tracking_url')
            
            if tracking_id and tracking_url:
                print("✅ Bağlantı oluşturma API çalışıyor")
                print(f"   Tracking ID: {tracking_id}")
                print(f"   Tracking URL: {tracking_url}")
                return tracking_id, tracking_url
            else:
                print("❌ API yanıtında gerekli alanlar eksik")
                return None, None
        else:
            print(f"❌ API hata döndü: {response.status_code}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"❌ API'ye bağlanılamadı: {e}")
        return None, None

def test_tracking_page(tracking_url):
    """Takip sayfasının çalışıp çalışmadığını test et"""
    print("\n🔍 Takip sayfası testi...")
    try:
        response = requests.get(tracking_url, timeout=5)
        if response.status_code == 200:
            if "Bilgi Toplama Rızası" in response.text:
                print("✅ Takip sayfası çalışıyor")
                return True
            else:
                print("❌ Takip sayfası içeriği beklenen formatta değil")
                return False
        else:
            print(f"❌ Takip sayfası hata döndü: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Takip sayfasına bağlanılamadı: {e}")
        return False

def test_data_collection_api():
    """Veri toplama API'sini test et"""
    print("\n🔍 Veri toplama API testi...")
    try:
        response = requests.get(
            f"{WEB_SERVER_URL}/api/get_collected_data/{TEST_USER_ID}",
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Veri toplama API çalışıyor")
            print(f"   Toplam bağlantı sayısı: {len(data)}")
            
            total_collected = sum(len(link.get('collected_data', [])) for link in data)
            print(f"   Toplanan veri sayısı: {total_collected}")
            return True
        else:
            print(f"❌ Veri toplama API hata döndü: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Veri toplama API'sine bağlanılamadı: {e}")
        return False

def test_database_integrity():
    """Veritabanı bütünlüğünü test et"""
    print("\n🔍 Veritabanı bütünlük testi...")
    
    # Birden fazla bağlantı oluştur
    tracking_ids = []
    for i in range(3):
        data = {"sender_telegram_id": TEST_USER_ID + i}
        try:
            response = requests.post(
                f"{WEB_SERVER_URL}/api/create_link",
                json=data,
                timeout=5
            )
            if response.status_code == 200:
                result = response.json()
                tracking_ids.append(result.get('tracking_id'))
        except:
            pass
    
    if len(tracking_ids) == 3:
        print("✅ Veritabanı bütünlüğü testi başarılı")
        print(f"   Oluşturulan tracking ID'ler: {len(tracking_ids)}")
        return True
    else:
        print(f"❌ Veritabanı bütünlük testi başarısız: {len(tracking_ids)}/3")
        return False

def run_all_tests():
    """Tüm testleri çalıştır"""
    print("🚀 Bilgi Toplama Botu - Entegrasyon Testleri Başlıyor\n")
    print("=" * 60)
    
    tests = [
        ("Web Sunucusu Sağlık", test_web_server_health),
        ("Bağlantı Oluşturma API", lambda: test_create_link_api()[0] is not None),
        ("Veri Toplama API", test_data_collection_api),
        ("Veritabanı Bütünlük", test_database_integrity),
    ]
    
    # Takip sayfası testi için bağlantı oluştur
    tracking_id, tracking_url = test_create_link_api()
    if tracking_url:
        tests.append(("Takip Sayfası", lambda: test_tracking_page(tracking_url)))
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} testi hata verdi: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Sonuçları: {passed}/{total} test başarılı")
    
    if passed == total:
        print("🎉 Tüm testler başarılı! Sistem hazır.")
        return True
    else:
        print("⚠️  Bazı testler başarısız. Lütfen hataları kontrol edin.")
        return False

def print_system_info():
    """Sistem bilgilerini yazdır"""
    print("\n📋 Sistem Bilgileri:")
    print(f"   Web Sunucusu: {WEB_SERVER_URL}")
    print(f"   Test Kullanıcı ID: {TEST_USER_ID}")
    print(f"   Ana Sayfa: {WEB_SERVER_URL}/")
    print(f"   API Endpoint: {WEB_SERVER_URL}/api/create_link")

if __name__ == "__main__":
    success = run_all_tests()
    print_system_info()
    
    if success:
        print("\n✅ Sistem entegrasyonu tamamlandı ve test edildi!")
        print("\n📝 Sonraki Adımlar:")
        print("   1. Telegram bot token'ınızı bot/telegram_bot.py dosyasına ekleyin")
        print("   2. Bot'u çalıştırın: python bot/telegram_bot.py")
        print("   3. Telegram'da botunuza /start komutu gönderin")
        sys.exit(0)
    else:
        print("\n❌ Sistem entegrasyonunda sorunlar var!")
        sys.exit(1)

