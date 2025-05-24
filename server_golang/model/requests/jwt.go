package requests

import "github.com/golang-jwt/jwt/v5"

type CustomClaims struct {
	BaseClaims
	jwt.RegisteredClaims
}

type BaseClaims struct {
	ID       uint
	Username string
}
