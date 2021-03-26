#!/usr/bin/python3

from brownie import NFPLToken, accounts


def main():
    return NFPLToken.deploy(accounts[1], accounts[2], {'from': accounts[0]})
