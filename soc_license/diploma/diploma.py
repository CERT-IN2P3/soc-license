from uuid import uuid4
from datetime import datetime
from fpdf import FPDF
from diploma.models import Diploma
from soc_license.settings import SOC_LICENSE
import hashlib
import base64
import rsa
import json


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
    def __init__(self, session, uuid=None):
        if uuid is None:
            self.uuid = str(uuid4())
        else:
            self.uuid = uuid
        self.session = session
        self.pdf = None
        self.signature = None
        self.date = datetime.now()

    def file(self):
        self.pdf = FPDF(orientation='L', unit='mm', format='A5')
        self.pdf.set_margin(0)
        self.pdf.add_page()
        self.pdf.set_font('helvetica', size=50)
        self.pdf.set_text_color(**COLOR['primary'])
        self.pdf.set_x(0)
        self.pdf.set_y(10)
        self.pdf.cell(txt="Certificat de diplôme",
                      new_y="NEXT",
                      new_x="LMARGIN",
                      w=0,
                      h=50,
                      align='C')
        self.pdf.set_font('helvetica', size=10)
        self.pdf.set_text_color(**COLOR['secondary'])
        self.pdf.cell(txt="Cela certifie que",
                      new_y="NEXT",
                      new_x="LMARGIN",
                      w=0,
                      align='C')
        self.pdf.set_font('helvetica', size=35)
        self.pdf.set_text_color(**COLOR['primary'])
        self.pdf.cell(txt="{firstname} {lastname}".format(firstname=self.session['firstname'],
                                                          lastname=self.session['lastname']),
                      new_y="NEXT",
                      new_x="LMARGIN",
                      w=0,
                      align='C')
        self.pdf.set_font('helvetica', size=10)
        self.pdf.set_text_color(**COLOR['secondary'])
        self.pdf.cell(txt="a réussi l'examen du brevet internet",
                      new_y="NEXT",
                      new_x="LMARGIN",
                      w=0,
                      align='C')
        self.pdf.cell(txt="de l'IN2P3.",
                      new_y="NEXT",
                      new_x="LMARGIN",
                      w=0,
                      align='C')
        self.pdf.set_y(95)
        self.pdf.set_x(170)
        self.pdf.set_text_color(**COLOR['tertiary'])
        self.pdf.cell(txt="Le {date}".format(date=self.date.date().strftime("%d/%m/%Y")),
                      new_y="NEXT",
                      new_x="LMARGIN",
                      align='C')
        self.pdf.set_y(95)
        self.pdf.set_x(20)
        self.pdf.set_text_color(**COLOR['tertiary'])
        self.pdf.cell(txt="Signature",
                      new_y="NEXT",
                      new_x="LMARGIN",
                      align='C')
        self.pdf.set_font('helvetica', size=6)
        self.pdf.image('./core/static/soc-license-badge.png',
                       x=120,
                       y=80,
                       w=50)
        self.pdf.set_y(135)
        self.pdf.set_x(150)
        self.pdf.cell(txt="uuid:{pdfname}".format(pdfname=self.uuid),
                      h=8)
        self.pdf.line(15, 15, 195, 15)
        self.pdf.line(15, 133, 195, 133)
        self.pdf.set_y(-25)
        self.pdf.set_x(0)
        self.pdf.image('./core/static/brand-logo.png',
                       x=15,
                       y=135,
                       w=12)
        self.pdf.set_y(100)
        self.pdf.set_x(20)
        self.pdf.set_text_color(**COLOR['tertiary'])
        self.pdf.multi_cell(txt=str(self.signature.decode("utf-8")),
                            new_y="NEXT",
                            new_x="LMARGIN",
                            w=50,
                            border=0,
                            align='L')
        self.pdf.output("{basedir}/{uuid}.pdf".format(basedir=SOC_LICENSE['diploma'], uuid=self.uuid))

    def sha512sum(self):
        sha512 = hashlib.sha512(
            open("{basedir}/{uuid}.pdf".format(basedir=SOC_LICENSE['diploma'], uuid=self.uuid), 'rb').read()).hexdigest()
        sha512_file = open("{basedir}/{uuid}.sha512".format(basedir=SOC_LICENSE['diploma'], uuid=self.uuid), 'w')
        sha512_file.write("{sha512}\n".format(sha512=sha512))
        sha512_file.close()
        diploma = Diploma.objects.create(uuid=self.uuid, sha512sum=sha512)
        diploma.save()

    def sign(self):
        with open('./config/diploma.pub', mode='rb') as signkeyfile:
            keydata = signkeyfile.read()
        signkey = rsa.PublicKey.load_pkcs1(keydata)
        if self.session["score"] < SOC_LICENSE['threshold']['advanced']:
            level = 'basic'
        elif self.session["score"] < SOC_LICENSE['threshold']['expert']:
            level = 'advanced'
        else:
            level = 'expert'
        token = {
            'firstname': self.session['firstname'],
            'lastname': self.session['lastname'],
            'date': self.date.strftime("%d/%m/%Y"),
            'level': level,
            'uuid': self.uuid
        }
        crypto_token = rsa.encrypt(json.dumps(token).encode('utf-8'), signkey)
        self.signature = base64.b64encode(crypto_token)

    @staticmethod
    def unsign(token):
        with open('./config/diploma.key', mode='rb') as unsignkeyfile:
            keydata = unsignkeyfile.read()
        unsignkey = rsa.PrivateKey.load_pkcs1(keydata)
        decode_signature = base64.b64decode(token)
        result = dict()
        try:
            uncrypt_signature = rsa.decrypt(decode_signature, unsignkey)
            result = json.loads(uncrypt_signature)
            result['status'] = 'success'
        except rsa.DecryptionError:
            result['status'] = 'error'
            result['message'] = 'signature error: Invalid signature'
        return result


def generate_license(session):
    today = datetime.now()
    filename = str(uuid.uuid4())
    pdf = FPDF(orientation='L', unit='mm', format='A5')
    pdf.set_margin(0)
    pdf.add_page()
    pdf.set_font('helvetica', size=50)
    pdf.set_text_color(**COLOR['primary'])
    pdf.set_x(0)
    pdf.set_y(10)
    pdf.cell(txt="Certificat de diplôme",
             new_y="NEXT",
             new_x="LMARGIN",
             w=0,
             h=50,
             align='C')
    pdf.set_font('helvetica', size=10)
#    pdf.set_text_color(r=70, g=74, b=76)
    pdf.set_text_color(**COLOR['secondary'])
    pdf.cell(txt="Cela certifie que",
             new_y="NEXT",
             new_x="LMARGIN",
             w=0,
             align='C')
    pdf.set_font('helvetica', size=35)
    pdf.set_text_color(**COLOR['primary'])
    pdf.cell(txt="{firstname} {lastname}".format(firstname=session['firstname'],
                                                 lastname=session['lastname']),
             new_y="NEXT",
             new_x="LMARGIN",
             w=0,
             align='C')
    pdf.set_font('helvetica', size=10)
#    pdf.set_text_color(r=70, g=74, b=76)
    pdf.set_text_color(**COLOR['secondary'])
    pdf.cell(txt="a réussi l'examen du brevet internet",
             new_y="NEXT",
             new_x="LMARGIN",
             w=0,
             align='C')
    pdf.cell(txt="de l'IN2P3.",
             new_y="NEXT",
             new_x="LMARGIN",
             w=0,
             align='C')
    pdf.set_y(95)
    pdf.set_x(170)
    pdf.set_text_color(**COLOR['tertiary'])
    pdf.cell(txt="Le {date}".format(date=today.date().strftime("%d/%m/%Y")),
             new_y="NEXT",
             new_x="LMARGIN",
             align='C')
    pdf.set_y(95)
    pdf.set_x(20)
    pdf.set_text_color(**COLOR['tertiary'])
    pdf.cell(txt="Signature",
             new_y="NEXT",
             new_x="LMARGIN",
             align='C')
    pdf.set_font('helvetica', size=6)
    pdf.image('./core/static/soc-license-badge.png',
              x=120,
              y=80,
              w=50)
    pdf.set_y(135)
    pdf.set_x(150)
    pdf.cell(txt="uuid:{pdfname}".format(pdfname=filename),
             h=8)
    pdf.line(15, 15, 195, 15)
    pdf.line(15, 133, 195, 133)
    pdf.set_y(-25)
    pdf.set_x(0)
    pdf.image('./core/static/brand-logo.png',
              x=15,
              y=135,
              w=12)
    with open('./config/diploma.pub', mode='rb') as privatefile:
        keydata = privatefile.read()
    privkey = rsa.PublicKey.load_pkcs1(keydata)
    token = {
        'firstname': session['firstname'],
        'lastname': session['lastname'],
        'date': today.strftime("%d/%m/%Y"),
        'score': session['score']
    }
    crypto = rsa.encrypt(json.dumps(token).encode('utf-8'), privkey)
    crypto_base64 = base64.b64encode(crypto)
    print(crypto_base64)
    pdf.set_y(100)
    pdf.set_x(20)
    pdf.set_text_color(**COLOR['tertiary'])
    pdf.multi_cell(txt=str(crypto_base64.decode("utf-8")),
                   new_y="NEXT",
                   new_x="LMARGIN",
                   w=50,
                   border=0,
                   align='L')
    pdf.output("./diplomas/{pdfname}.pdf".format(pdfname=filename))
    sha512sum = hashlib.sha512(open("./diplomas/{pdfname}.pdf".format(pdfname=filename), 'rb').read()).hexdigest()
    sha512_file = open("./diplomas/{pdfname}.sha512".format(pdfname=filename), 'w')
    sha512_file.write("{sha512}\n".format(sha512=sha512sum))
    sha512_file.close()
    diploma = Diploma.objects.create(uuid=filename, sha512sum=sha512sum)
    diploma.save()
    return filename


def check_diploma(signature):
    with open('./config/diploma.key', mode='rb') as publickey:
        pubdata = publickey.read()
    pubkey = rsa.PrivateKey.load_pkcs1(pubdata)
    decode_signature = base64.b64decode(signature)
    decrypt_signature = rsa.decrypt(decode_signature, pubkey)
    print(decrypt_signature)