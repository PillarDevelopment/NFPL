#!/usr/bin/python3
import brownie


def test_sender_balance_decreases(accounts, NFPLToken):
    sender_balance = NFPLToken.balanceOf(accounts[0])
    amount = sender_balance // 4

    NFPLToken.approve(accounts[1], amount, {'from': accounts[0]})
    NFPLToken.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert NFPLToken.balanceOf(accounts[0]) == sender_balance - amount


def test_receiver_balance_increases(accounts, NFPLToken):
    receiver_balance = NFPLToken.balanceOf(accounts[2])
    amount = NFPLToken.balanceOf(accounts[0]) // 4

    NFPLToken.approve(accounts[1], amount, {'from': accounts[0]})
    NFPLToken.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert NFPLToken.balanceOf(accounts[2]) == receiver_balance + amount


def test_caller_balance_not_affected(accounts, NFPLToken):
    caller_balance = NFPLToken.balanceOf(accounts[1])
    amount = NFPLToken.balanceOf(accounts[0])

    NFPLToken.approve(accounts[1], amount, {'from': accounts[0]})
    token.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert token.balanceOf(accounts[1]) == caller_balance


def test_caller_approval_affected(accounts, NFPLToken):
    approval_amount = NFPLToken.balanceOf(accounts[0])
    transfer_amount = approval_amount // 4

    NFPLToken.approve(accounts[1], approval_amount, {'from': accounts[0]})
    NFPLToken.transferFrom(accounts[0], accounts[2], transfer_amount, {'from': accounts[1]})

    assert NFPLToken.allowance(accounts[0], accounts[1]) == approval_amount - transfer_amount


def test_receiver_approval_not_affected(accounts, token):
    approval_amount = NFPLToken.balanceOf(accounts[0])
    transfer_amount = approval_amount // 4

    NFPLToken.approve(accounts[1], approval_amount, {'from': accounts[0]})
    NFPLToken.approve(accounts[2], approval_amount, {'from': accounts[0]})
    NFPLToken.transferFrom(accounts[0], accounts[2], transfer_amount, {'from': accounts[1]})

    assert NFPLToken.allowance(accounts[0], accounts[2]) == approval_amount


def test_total_supply_not_affected(accounts, NFPLToken):
    total_supply = NFPLToken.totalSupply()
    amount = NFPLToken.balanceOf(accounts[0])

    NFPLToken.approve(accounts[1], amount, {'from': accounts[0]})
    NFPLToken.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert NFPLToken.totalSupply() == total_supply


def test_returns_true(accounts, NFPLToken):
    amount = NFPLToken.balanceOf(accounts[0])
    NFPLToken.approve(accounts[1], amount, {'from': accounts[0]})
    tx = NFPLToken.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert tx.return_value is True


def test_transfer_full_balance(accounts, NFPLToken):
    amount = NFPLToken.balanceOf(accounts[0])
    receiver_balance = NFPLToken.balanceOf(accounts[2])

    NFPLToken.approve(accounts[1], amount, {'from': accounts[0]})
    NFPLToken.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert NFPLToken.balanceOf(accounts[0]) == 0
    assert NFPLToken.balanceOf(accounts[2]) == receiver_balance + amount


def test_transfer_zero_tokens(accounts, NFPLToken):
    sender_balance = NFPLToken.balanceOf(accounts[0])
    receiver_balance = NFPLToken.balanceOf(accounts[2])

    NFPLToken.approve(accounts[1], sender_balance, {'from': accounts[0]})
    NFPLToken.transferFrom(accounts[0], accounts[2], 0, {'from': accounts[1]})

    assert NFPLToken.balanceOf(accounts[0]) == sender_balance
    assert NFPLToken.balanceOf(accounts[2]) == receiver_balance


def test_transfer_zero_tokens_without_approval(accounts, NFPLToken):
    sender_balance = NFPLToken.balanceOf(accounts[0])
    receiver_balance = NFPLToken.balanceOf(accounts[2])

    NFPLToken.transferFrom(accounts[0], accounts[2], 0, {'from': accounts[1]})

    assert NFPLToken.balanceOf(accounts[0]) == sender_balance
    assert NFPLToken.balanceOf(accounts[2]) == receiver_balance


def test_insufficient_balance(accounts, NFPLToken):
    balance = NFPLToken.balanceOf(accounts[0])

    NFPLToken.approve(accounts[1], balance + 1, {'from': accounts[0]})
    with brownie.reverts():
        NFPLToken.transferFrom(accounts[0], accounts[2], balance + 1, {'from': accounts[1]})


def test_insufficient_approval(accounts, NFPLToken):
    balance = NFPLToken.balanceOf(accounts[0])

    NFPLToken.approve(accounts[1], balance - 1, {'from': accounts[0]})
    with brownie.reverts():
        NFPLToken.transferFrom(accounts[0], accounts[2], balance, {'from': accounts[1]})


def test_no_approval(accounts, NFPLToken):
    balance = NFPLToken.balanceOf(accounts[0])

    with brownie.reverts():
        NFPLToken.transferFrom(accounts[0], accounts[2], balance, {'from': accounts[1]})


def test_revoked_approval(accounts, NFPLToken):
    balance = NFPLToken.balanceOf(accounts[0])

    NFPLToken.approve(accounts[1], balance, {'from': accounts[0]})
    NFPLToken.approve(accounts[1], 0, {'from': accounts[0]})

    with brownie.reverts():
        NFPLToken.transferFrom(accounts[0], accounts[2], balance, {'from': accounts[1]})


def test_transfer_to_self(accounts, NFPLToken):
    sender_balance = NFPLToken.balanceOf(accounts[0])
    amount = sender_balance // 4

    NFPLToken.approve(accounts[0], sender_balance, {'from': accounts[0]})
    NFPLToken.transferFrom(accounts[0], accounts[0], amount, {'from': accounts[0]})

    assert NFPLToken.balanceOf(accounts[0]) == sender_balance
    assert NFPLToken.allowance(accounts[0], accounts[0]) == sender_balance - amount


def test_transfer_to_self_no_approval(accounts, NFPLToken):
    amount = NFPLToken.balanceOf(accounts[0])

    with brownie.reverts():
        NFPLToken.transferFrom(accounts[0], accounts[0], amount, {'from': accounts[0]})


def test_transfer_event_fires(accounts, NFPLToken):
    amount = NFPLToken.balanceOf(accounts[0])

    NFPLToken.approve(accounts[1], amount, {'from': accounts[0]})
    tx = NFPLToken.transferFrom(accounts[0], accounts[2], amount, {'from': accounts[1]})

    assert len(tx.events) == 1
    assert tx.events["Transfer"].values() == [accounts[0], accounts[2], amount]
