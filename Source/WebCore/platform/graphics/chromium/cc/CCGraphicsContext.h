/*
 * Copyright (C) 2012 Google Inc. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1.  Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 * 2.  Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY APPLE AND ITS CONTRIBUTORS "AS IS" AND ANY
 * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL APPLE OR ITS CONTRIBUTORS BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 * THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef CCGraphicsContext_h
#define CCGraphicsContext_h

#include <public/WebGraphicsContext3D.h>
#include <wtf/Noncopyable.h>
#include <wtf/OwnPtr.h>
#include <wtf/PassOwnPtr.h>

namespace WebCore {


class CCGraphicsContext {
    WTF_MAKE_NONCOPYABLE(CCGraphicsContext);
public:
    static PassOwnPtr<CCGraphicsContext> create2D()
    {
        return adoptPtr(new CCGraphicsContext());
    }
    static PassOwnPtr<CCGraphicsContext> create3D(PassOwnPtr<WebKit::WebGraphicsContext3D> context3D)
    {
        return adoptPtr(new CCGraphicsContext(context3D));
    }

    WebKit::WebGraphicsContext3D* context3D() { return m_context3D.get(); }

    void flush()
    {
        if (m_context3D)
            m_context3D->flush();
    }

private:
    CCGraphicsContext() { }
    explicit CCGraphicsContext(PassOwnPtr<WebKit::WebGraphicsContext3D> context3D)
        : m_context3D(context3D) { }

    OwnPtr<WebKit::WebGraphicsContext3D> m_context3D;
};

}

#endif // CCGraphicsContext_h
