package utils

import (
	"errors"
	"github.com/golang-jwt/jwt/v5"
	"server_golang/model/requests"
	"time"
)

type JWT struct {
	SigningKey []byte
}

var (
	TokenValid            = errors.New("未知错误")
	TokenExpired          = errors.New("token已过期")
	TokenNotValidYet      = errors.New("token尚未激活")
	TokenMalformed        = errors.New("这不是一个token")
	TokenSignatureInvalid = errors.New("无效签名")
	TokenInvalid          = errors.New("无法处理此token")
)

func NewJWT() *JWT {
	return &JWT{
		[]byte("my secret key"),
	}
}

func (j *JWT) CreateClaims(baseClaims requests.BaseClaims) requests.CustomClaims {
	claims := requests.CustomClaims{
		BaseClaims: baseClaims,
		//BufferTime: int64(bf / time.Second), // 缓冲时间1天 缓冲时间内会获得新的token刷新令牌 此时一个用户会存在两个有效令牌 但是前端只留一个 另一个会丢失
		RegisteredClaims: jwt.RegisteredClaims{
			Audience:  jwt.ClaimStrings{"GVA"},                                // 受众
			NotBefore: jwt.NewNumericDate(time.Now().Add(-1000)),              // 签名生效时间
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(time.Hour * 24 * 7)), // 过期时间 7天  配置文件
			Issuer:    "yubo.zha",                                             // 签名的发行者
		},
	}
	return claims
}

// CreateToken 创建一个token
func (j *JWT) CreateToken(claims requests.CustomClaims) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(j.SigningKey)
}

// CreateTokenByOldToken 旧token 换新token 使用归并回源避免并发问题
//func (j *JWT) CreateTokenByOldToken(oldToken string, claims model.CustomClaims) (string, error) {
//	v, err, _ := global.GVA_Concurrency_Control.Do("JWT:"+oldToken, func() (interface{}, error) {
//		return j.CreateToken(claims)
//	})
//	return v.(string), err
//}

// ParseToken 解析 token
func (j *JWT) ParseToken(tokenString string) (*requests.CustomClaims, error) {
	token, err := jwt.ParseWithClaims(tokenString, &requests.CustomClaims{}, func(token *jwt.Token) (i interface{}, e error) {
		return j.SigningKey, nil
	})

	if err != nil {
		switch {
		case errors.Is(err, jwt.ErrTokenExpired):
			return nil, TokenExpired
		case errors.Is(err, jwt.ErrTokenMalformed):
			return nil, TokenMalformed
		case errors.Is(err, jwt.ErrTokenSignatureInvalid):
			return nil, TokenSignatureInvalid
		case errors.Is(err, jwt.ErrTokenNotValidYet):
			return nil, TokenNotValidYet
		default:
			return nil, TokenInvalid
		}
	}
	if token != nil {
		if claims, ok := token.Claims.(*requests.CustomClaims); ok && token.Valid {
			return claims, nil
		}
	}
	return nil, TokenValid
}
