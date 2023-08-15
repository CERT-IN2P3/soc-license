from uuid import uuid4
from datetime import datetime
from fpdf import FPDF
from diploma.models import Diploma
from soc_license.settings import SOC_LICENSE
import hashlib
import base64
import rsa
import json
import os

COLOR = {
    'primary': {
        'r': 2,
        'g': 30,
        'b': 58
    },
    'secondary': {
        'r': 69,
        'g': 100,
        'b': 135
    },
    'tertiary': {
        'r': 70,
        'g': 74,
        'b': 76
    }
}


class DiplomaCtrl(object):
    def __init__(self, session, uuid=None, signature=None):
        # We initialize the diploma
        self.session = session
        self.firstname = None
        self.lastname = None
        self.date = None
        self.level = None
        self.diploma = None
        self.pubkey = None

        if uuid is None:
            # If uuid is not set, so it should be a diploma creation
            self.create()
        else:
            # else, we load information from models
            self.uuid = uuid
            if signature is not None:
                self.signature = signature
            else:
                self.signature = session['signature']
            self.diploma = Diploma.objects.get(uuid=self.uuid)
            self.unsign()
            self.pubkey = None

    def create(self):
        self.uuid = str(uuid4())
        self.firstname = self.session['firstname']
        self.lastname = self.session['lastname']
        self.date = datetime.now()
        if self.session["score"] < SOC_LICENSE['threshold']['advanced']:
            self.level = 'basic'
        elif self.session["score"] < SOC_LICENSE['threshold']['expert']:
            self.level = 'advanced'
        else:
            self.level = 'expert'

        self.diploma = Diploma(uuid=self.uuid)
        self.generate_keys()
        self.sign()
        self.diploma.save()

    def get(self, format='json'):
        certificate = self.unsign()
        if format == 'json':
            return certificate
        elif format == 'pdf':
            return self.pdf(certificate)

    def pdf(self, certificate):
        file = FPDF(orientation='L', unit='mm', format='A5')
        file.set_margin(0)
        file.add_page()
        file.set_font('helvetica', size=50)
        file.set_text_color(**COLOR['primary'])
        file.set_x(0)
        file.set_y(10)
        file.cell(txt=SOC_LICENSE['diploma']['pdf']['line1'],
                  new_y="NEXT",
                  new_x="LMARGIN",
                  w=0,
                  h=50,
                  align='C')
        file.set_font('helvetica', size=10)
        file.set_text_color(**COLOR['secondary'])
        file.cell(txt=SOC_LICENSE['diploma']['pdf']['line2'],
                  new_y="NEXT",
                  new_x="LMARGIN",
                  w=0,
                  align='C')
        file.set_font('helvetica', size=35)
        file.set_text_color(**COLOR['primary'])
        file.cell(txt="{firstname} {lastname}".format(firstname=certificate['firstname'],
                                                      lastname=certificate['lastname']),
                  new_y="NEXT",
                  new_x="LMARGIN",
                  w=0,
                  align='C')
        file.set_font('helvetica', size=10)
        file.set_text_color(**COLOR['secondary'])
        file.cell(txt=SOC_LICENSE['diploma']['pdf']['line3'],
                  new_y="NEXT",
                  new_x="LMARGIN",
                  w=0,
                  align='C')
        file.cell(txt=SOC_LICENSE['diploma']['pdf']['line4'],
                  new_y="NEXT",
                  new_x="LMARGIN",
                  w=0,
                  align='C')
        file.set_y(95)
        file.set_x(170)
        file.set_text_color(**COLOR['tertiary'])
        file.cell(txt="Date : {date}".format(date=certificate['date']),
                  new_y="NEXT",
                  new_x="LMARGIN",
                  align='C')
        file.set_y(95)
        file.set_x(20)
        file.set_text_color(**COLOR['tertiary'])
        file.cell(txt="Signature",
                  new_y="NEXT",
                  new_x="LMARGIN",
                  align='C')
        file.set_font('helvetica', size=6)
        file.image(SOC_LICENSE['diploma']['pdf']['badge'],
                   x=150,
                   y=95,
                   w=25)
        file.set_y(135)
        file.set_x(150)
        file.cell(txt="{pdfname}".format(pdfname=self.uuid),
                  h=8)
        file.line(15, 15, 195, 15)
        file.line(15, 133, 195, 133)
        file.set_y(-25)
        file.set_x(0)
        file.image(SOC_LICENSE['diploma']['pdf']['brand'],
                   x=15,
                   y=135,
                   h=12)
        file.set_y(100)
        file.set_x(20)
        file.set_text_color(**COLOR['tertiary'])
        file.multi_cell(txt=str(self.signature),
                        new_y="NEXT",
                        new_x="LMARGIN",
                        w=50,
                        border=0,
                        align='L')
        file.output("{basedir}/{uuid}.pdf".format(basedir=SOC_LICENSE['diploma']['basedir'],
                                                  uuid=self.uuid))
        with open('{basedir}/{uuid}.pdf'.format(
                                 basedir=SOC_LICENSE['diploma']['basedir'],
                                 uuid=self.uuid), 'rb') as filename:
            result = filename.read()
            filename.close()
            os.unlink('{basedir}/{uuid}.pdf'.format(basedir=SOC_LICENSE['diploma']['basedir'],
                                                    uuid=self.uuid))
        return result

    def sha512sum(self):
        pass

    def sign(self):
        if self.session["score"] < SOC_LICENSE['threshold']['advanced']:
            level = 'basic'
        elif self.session["score"] < SOC_LICENSE['threshold']['expert']:
            level = 'advanced'
        else:
            level = 'expert'
        certificate = {
            'firstname': self.session['firstname'],
            'lastname': self.session['lastname'],
            'date': self.date.strftime("%d/%m/%Y"),
            'level': level,
            'uuid': self.uuid
        }
        crypto_token = rsa.encrypt(json.dumps(certificate).encode('utf-8'),
                                   self.pubkey)
        self.signature = base64.b64encode(crypto_token).decode('utf-8')

    def unsign(self):
        decode_signature = base64.b64decode(self.signature)
        result = dict()
        try:
            uncrypt_signature = rsa.decrypt(decode_signature,
                                            rsa.PrivateKey.load_pkcs1(self.diploma.private_key))
            result = json.loads(uncrypt_signature)
            result['signature'] = self.signature
            result['status'] = 'success'
        except rsa.DecryptionError:
            result['status'] = 'error'
            result['message'] = 'signature error: Invalid signature'
        return result

    def generate_keys(self):
        (self.pubkey, private_key) = rsa.newkeys(2048, poolsize=2)
        self.diploma.private_key = rsa.PrivateKey.save_pkcs1(private_key).decode('utf-8')
