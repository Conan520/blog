package utils

import (
	"github.com/bwmarrin/snowflake"
	"github.com/sony/sonyflake/v2"
)

var flake *sonyflake.Sonyflake

func GenerateID() (int64, error) {
	node, err := snowflake.NewNode(1)
	if err != nil {
		return 0, err
	}
	return node.Generate().Int64(), nil
}

func GenerateFlakeId() (int64, error) {
	id, err := flake.NextID()
	return id, err
}

func init() {
	var err error
	flake, err = sonyflake.New(sonyflake.Settings{})
	if err != nil {
		panic(err)
	}
}
