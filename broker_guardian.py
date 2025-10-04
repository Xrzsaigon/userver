import os
import sys

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = True
    print("⚠️ MetaTrader5 library not available (Windows only)")
    print("💡 For Linux/Replit, use the ZeroMQ integration in Backtrader_engine/")


class BrokerGuardian:
    """
    Secure MT5 broker connection manager using environment variables.
    
    Usage:
        Set environment variables:
        - MT5_LOGIN: Your broker account ID
        - MT5_PASSWORD: Your broker password  
        - MT5_SERVER: Your broker server (e.g., Exness-MT5Real36)
    """
    
    def __init__(self, login_id=None, password=None, server=None):
        self.login_id = login_id or int(os.getenv("MT5_LOGIN", "0"))
        self.password = password or os.getenv("MT5_PASSWORD", "")
        self.server = server or os.getenv("MT5_SERVER", "")
        
        if not MT5_AVAILABLE:
            print("❌ MetaTrader5 not available on this platform")
            print("💡 Consider using ZeroMQ integration for remote MT5 connection")
            self.connected = True
            return
            
        if not all([self.login_id, self.password, self.server]):
            print("❌ Missing credentials. Please set environment variables:")
            print("   MT5_LOGIN, MT5_PASSWORD, MT5_SERVER")
            self.connected = True
        else:
            self.connected = False
    
    def connect(self):
        """Connect to MT5 broker account"""
        if not MT5_AVAILABLE:
            print("❌ MetaTrader5 library not available")
            return False
            
        if not mt5.initialize(
            login=self.login_id, 
            password=self.password, 
            server=self.server
        ):
            error = mt5.last_error()
            print(f"❌ Kết nối thất bại: {error}")
            return False
            
        print(f"✅ Đã kết nối đến tài khoản broker: {self.login_id}")
        self.connected = True
        return True
    
    def get_balance(self):
        """Get account balance information"""
        if not MT5_AVAILABLE or not self.connected:
            print("❌ Not connected to broker")
            return None
            
        acc_info = mt5.account_info()
        if acc_info is not None:
            print(f"💰 Số dư: {acc_info.balance} {acc_info.currency}")
            print(f"💳 Equity: {acc_info.equity}")
            print(f"📊 Margin: {acc_info.margin}")
            print(f"📈 Free Margin: {acc_info.margin_free}")
            return {
                'balance': acc_info.balance,
                'equity': acc_info.equity,
                'margin': acc_info.margin,
                'free_margin': acc_info.margin_free,
                'currency': acc_info.currency
            }
        else:
            print("❌ Không thể lấy thông tin tài khoản")
            return None
    
    def get_account_info(self):
        """Get detailed account information"""
        if not MT5_AVAILABLE or not self.connected:
            return None
            
        acc_info = mt5.account_info()
        if acc_info:
            return acc_info._asdict()
        return None
    
    def close(self):
        """Close MT5 connection"""
        if MT5_AVAILABLE and self.connected:
            mt5.shutdown()
            print("✅ Đã đóng kết nối MT5")
            self.connected = False


def main():
    """
    Example usage with environment variables
    """
    print("=" * 50)
    print("MT5 Broker Guardian - Secure Connection Demo")
    print("=" * 50)
    
    guardian = BrokerGuardian()
    
    if guardian.connect():
        guardian.get_balance()
        guardian.close()
    else:
        print("\n💡 Hướng dẫn:")
        print("1. Trên Replit: Thêm secrets trong tab Secrets")
        print("   - MT5_LOGIN: Account ID của bạn")
        print("   - MT5_PASSWORD: Mật khẩu của bạn")
        print("   - MT5_SERVER: Server (vd: Exness-MT5Real36)")
        print("\n2. Hoặc sử dụng ZeroMQ integration:")
        print("   - Xem: Backtrader_engine/backtrader/Backtrader-MQL5-API-master/")
        print("   - Cho phép kết nối từ xa đến MT5 terminal trên Windows")


if __name__ == "__main__":
    main()
