WARNING!!!! THIS IS IN DEVELOPMENT!!!!
======================================


secprov: Secure Provisioning of machines
========================================

This tool uses the machine's TPM and/or a users' Yubikey (NEO/4) to securely
provision a machine.

This can set up the following things:
- Set the LUKS passphrase
- Set the root password
- Set the grub2 password
- Create a user for the machine owner
- Run a random command (for example: ansible)

Running it exists of two different steps:
1. Preparation
2. Provisioning


Preparation
-----------

Preparation is done before the provisioning of the (new) system, and depending
on what level of security you want you need access to multiple items:

- The serial number of the machine to provision as reported by the BIOS.
- If you want to use the TPM to seal the data, you need to run the preparation
  script on the computer to provision, and have the TPM setup.
- If you want to use a Yubikey to secure the data, you need to have the public
  certificate for the key on the Yubikey.

Note: it is not supported to skip both TPM and Yubikey, since that would mean
the provisioning data would be unencrypted, destroying the entire purpose of
this tool.

To prepare a system, run the ``secprov-prepare`` tool.

During preparation, you will be asked for the information you want configured
on the target machine and the "old" LUKS passphrase set by your kickstart.

This will then generate a JSON metadata document.
This document will be sealed with the TPM and/or encrypted for the public key
provided.

This encrypted document will be uploaded to the provisioning server, using the
sha256 hash of the machine's serial number as the identifier.
This means the provisioning server will only have a hash of the machine's
serial number and the encrypted binary blob.
Because of this, the provisioning server has no knowledge about the machine
data, and can be run in an untrusted environment.

Note: the provisioning server might be set up to require a challenge-response
during upload to prevent spammers. Because of this, uploading a new file might
take some time. (this is up to the configuration of the provisioning server)

With this, preparation has been completed, and the uploaded metadata can be
used to provision the machine as many times as wanted.


Provisioning
------------

The provisioning is done with the ``secprov`` tool, and should probably be run
as a systemd file upon boot (before the multi-user target), but after the tcsd
and/or pcscd daemons have started.

Please note: if a yubikey-stored key is used to encrypt the metadata, this
yubikey should be inserted BEFORE booting the system: the tool will by default
NOT wait for insertion of a yubikey, to prevent the system from booting in case
the yubikey got lost.

The provisioning tool will first retrieve the encrypted metadata file from the
provisioning server, using the same hash of the machines serial number to
retrieve the file.

After this, it will determine whether the file needs to be decrypted with the
TPM and/or a yubikey and do so.

After it decrypted the metadata file, it will perform the actions described in
the document, which were encoded there by the preparation process.
The provisioning process may take a while to complete, depending on the number
and kind of actions requested.

After the provisioning finished, it will reboot the system, after which it will
be ready to be used.

It will store its logs in /var/log/provision.log.


Servers
-------

The directory Servers ships example provision server implementations.


Hints (In progress)
-------------------

To create a new yubikey key and certificate:
- yubico-piv-tool --action=generate --slot=9e --hash=SHA256 --algorithm=RSA2048
- yubico-piv-tool --action=selfsign-certificate --slot=9e --subject="/CN=Provisioning Key/"
- yubico-piv-tool --action=import-certificate --slot=9e

Save the certificate from the second command, as you need to input that to secprov-prepare.

If you lost it, or generated it earlier, you can use:
yubico-piv-tool --action=read-certificate --slot=9e


Wishlist
--------

- Support for DEO encryption layer
